from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError, StatementError, DataError

from backend.utils.auth_helpers import get_current_user

from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.schemas import (
    GoalTaskCreateRequest,
    GoalTaskUpdateRequest,
    GoalsTasksOut,
    GoalRequestWithTasks,
    GoalTaskOrderUpdateRequest,
    GoalTaskStatusAndOrderUpdateRequest,
)
from ..models.models import GoalsTasks
from openai import OpenAI
import json
from ..repository.repository import (
    GoalTaskRepository,
    GoalRepository,
    GoalTaskNotFound,
    StatusUnchangedError,
)
from ..config import settings


router = APIRouter(prefix="/goal-tasks", tags=["goal-tasks"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

goal_task_repository = GoalTaskRepository()
goal_repository = GoalRepository()


@router.get("/{goal_id}", status_code=status.HTTP_200_OK)
def read_all_goal_tasks(user: user_dependency, db: db_dependency, goal_id: int):
    try:
        goal_tasks = goal_task_repository.fetch_goal_tasks_by_goal_id_from_db(
            db, goal_id
        )

        if not goal_tasks:
            raise HTTPException(
                status_code=404, detail="目標達成タスクが見つかりません"
            )

        return {"detail": "目標達成タスクを取得しました", "goal_tasks": goal_tasks}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが取得できません")


@router.delete("/{goal_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal_tasks(user: user_dependency, db: db_dependency, goal_task_id: int):
    try:
        goal_task = goal_task_repository.get_goal_task_by_goal_task_id_from_db(
            db, goal_task_id
        )

        if goal_task is None:
            raise HTTPException(
                status_code=404, detail="目標達成タスクが見つかりません"
            )

        goal_task_repository.delete_goal_task_from_db(db, goal_task, commit=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが削除できません")


@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_chat_reply(payload: GoalRequestWithTasks, user: user_dependency):
    try:
        client = OpenAI(
            # This is the default and can be omitted
            api_key=settings.OPENAI_API_KEY,
        )
        goal = payload.goal

        completed_goal_tasks = payload.completed_goal_tasks_list or []
        response = client.responses.create(
            model="gpt-5-mini",
            instructions="""あなたは目標達成のためのタスク設計コーチです。
            以下の入力（目標名／現在の状況／開始日／期限日／平日・休日の可用時間／生成条件）に基づき,
            現実的で実行可能なタスク群と日別配分案を作成してください。""",
            input=f"""入力
            - 目標名 {goal.goal_name}
            - 現在の状況 {goal.status_against_goal}
            - 開始日 {goal.start_day}
            - 期限日 {goal.target_day}
            - 平日可用時間(1日あたり) {goal.weekday_available_time}
            - 休日の可用時間(1日あたり 祝日法第3条第3項による休日も含める) {goal.weekends_available_time}
            - 生成条件（省略される場合あり） {goal.task_creation_rule}


            出力形式（JSON）
            - goal_tasks: タスク一覧（タスクの締め切りが早い順に並べる）
            - goal_task_name: 必ず100字以内のタスク名(参考書に関するアドバイスも付け加える)
            - deadline: date型 (YYYY-MM-DD)(開始日と期限日・平日可用時間と休日の可用時間を考慮して)
            - estimated_time: 実行時間(1日の平日可用時間もしくは休日の可用時間を合計で下回るか、それらの可用時間と同じになるようタスクを生成して)

            出力例
            {{
          "goal_tasks": [
            {{
              "goal_task_name": "基本情報技術者試験の動画視聴をする",
              "deadline": "2025-09-10",
              "estimated_time": 60
            }},
            {{
              "goal_task_name": "キタミ式イラストIT塾 基本情報技術者を読む",
              "deadline": "2025-09-11",
              "estimated_time": 25
            }},{{
              "goal_task_name": "過去問道場のサイトを利用して基本情報技術者試験の1問1答をする",
              "deadline": "2025-09-11",
              "estimated_time": 35
            }},
            {{
              "goal_task_name": "基本情報技術者試験の過去問を1年分解く",
              "deadline": "2025-09-12",
              "estimated_time": 90
            }}
          ]
        }}
            注意事項
            - 優先度は内部的に考慮するが、出力フィールドには含めない
            - タスクの内容は何をどこまでやるか実行可能なレベルで具体的に示す。
            - タスクに必要な資料や本は正しいものを挙げるが、タスク名は100字以内に収める
            - タスクは優先度が高い順に締め切りを早く設定して
            - 長時間の作業は分割して複数タスクにする
            - タスクの締め切りは開始日と期限日の間に設定し、期限日から逆算して設定する
            - 1日に複数種類のタスクを含めてもよいが、それらのタスクを合計して平日は平日可用時間と休日は休日の可用時間内に収める
            - 現実的な時間配分を守る
            - 生成条件が与えられない場合は無視してよい
            - 注意: daily_schedule は無視してください
            -{json.dumps(completed_goal_tasks, ensure_ascii=False, default=str)}は完了済みの目標達成タスクリストです。これらのタスクを考慮して不要な目標に向けた達成タスクは生成しない。
            完了済みタスクと同じ内容のタスクはなるべく生成しないでほしいが、必要に応じて再度該当のタスクを実施する必要がある場合は、完了済みタスクと同じ内容のタスクを生成しても構わないです。
            この{json.dumps(completed_goal_tasks, ensure_ascii=False, default=str)}は存在しない可能性もある。その場合は考慮しなくていい。
            """,
        )
        response_text = response.output_text
        try:
            print("OpenAI response:", response.output_text)
            tasks_json = json.loads(response_text)
        except json.JSONDecodeError:
            # シングルクオートをダブルクオートに置換して再トライ
            fixed_text = response_text.replace("'", '"')
            try:
                tasks_json = json.loads(fixed_text)
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=500, detail=f"JSON変換に失敗: {e}")
        goal_tasks = []
        for task in tasks_json["goal_tasks"]:
            goal_tasks.append(GoalsTasksOut(**task))

        return {
            "detail": "目標達成タスクを生成しました",
            "goal_tasks": goal_tasks,
            "goal": goal,
        }

    except HTTPException:
        raise
    except (
        ValueError,
        IntegrityError,
        DataError,
        GoalTaskNotFound,
        StatusUnchangedError,
    ) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e)}: タスクの生成に失敗しました"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_goal_task(
    user: user_dependency,
    db: db_dependency,
    payload: GoalTaskCreateRequest,
):
    try:
        goals = goal_repository.search_goal_by_user_id(db, user.get("user_id"))
        goal = goals[0] if goals else None
        if goal is None:
            raise HTTPException(status_code=404, detail="未達成の目標が見つかりません")

        existing_tasks = goal_task_repository.fetch_goal_tasks_by_goal_id_from_db(
            db, goal.goal_id
        )
        order_num = (
            len(
                [
                    task
                    for task in existing_tasks
                    if task.goal_task_status == payload.goal_task_status.value
                ]
            )
            + 1
        )

        goal_task = GoalsTasks(
            goal_id=goal.goal_id,
            order_num=order_num,
            goal_task_name=payload.goal_task_name,
            goal_task_status=payload.goal_task_status.value,
            deadline=payload.deadline,
            estimated_time=payload.estimated_time,
        )
        goal_task_repository.register_goal_task(db, [goal_task], commit=True)
        db.refresh(goal_task)

        return {
            "detail": "目標達成タスクを登録しました",
            "goal_task": {
                "goal_task_id": goal_task.goal_task_id,
                "goal_id": goal_task.goal_id,
                "order_num": goal_task.order_num,
                "goal_task_name": goal_task.goal_task_name,
                "goal_task_status": goal_task.goal_task_status,
                "deadline": goal_task.deadline.isoformat(),
                "estimated_time": goal_task.estimated_time,
            },
        }
    except HTTPException:
        raise
    except (ValueError, IntegrityError, StatementError, DataError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが登録されません")


@router.put("/order", status_code=status.HTTP_204_NO_CONTENT)
def update_goal_task_order(
    user: user_dependency,
    db: db_dependency,
    payload: GoalTaskOrderUpdateRequest,
):
    try:
        from_updated_task, to_updated_task = (
            goal_task_repository.update_goal_task_order_from_db(
                db,
                payload.from_goal_task_id,
                payload.to_goal_task_id,
                commit=True,
            )
        )

        if from_updated_task is None or to_updated_task is None:
            raise HTTPException(
                status_code=404, detail="目標達成タスクが見つかりません"
            )
    except HTTPException:
        raise
    except (ValueError, GoalTaskNotFound, StatusUnchangedError, DataError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが更新できません")


@router.put("/status/{goal_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_goal_task_status_and_order(
    user: user_dependency,
    db: db_dependency,
    goal_task_id: int,
    payload: GoalTaskStatusAndOrderUpdateRequest,
):
    try:
        updated_task = goal_task_repository.update_goal_task_status_and_order_from_db(
            db, goal_task_id, payload.new_status, payload.order_num, commit=True
        )

        if updated_task is None:
            raise HTTPException(
                status_code=404, detail="目標達成タスクが見つかりません"
            )
    except HTTPException:
        raise
    except (ValueError, GoalTaskNotFound, StatusUnchangedError, DataError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが更新できません")


@router.put("/{goal_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_goal_task(
    user: user_dependency,
    db: db_dependency,
    goal_task_id: int,
    payload: GoalTaskUpdateRequest,
):
    try:
        goal_task_repository = GoalTaskRepository()
        updated_task = goal_task_repository.update_goal_task_from_db(
            db,
            goal_task_id,
            payload.goal_task_name,
            payload.deadline,
            payload.estimated_time,
            commit=True,
        )

        if updated_task is None:
            raise HTTPException(
                status_code=404, detail="目標達成タスクが見つかりません"
            )
    except HTTPException:
        raise
    except (ValueError, GoalTaskNotFound, StatusUnchangedError, DataError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが更新できません")
