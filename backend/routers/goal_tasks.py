from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError, StatementError, DataError

from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.schemas import GoalsTasksOut, GoalRequestWithTasks, SaveRequest
from ..models.models import GoalsTasks, GoalsTasksStatusEnum, Goals, GoalsStatusEnum
from openai import OpenAI
import os
import json
from ..repository.repository import GoalTaskRepository, GoalRepository, GoalTaskNotFound, StatusUnchangedError
from .auth import get_current_user

router = APIRouter(
    prefix="/goal_tasks",
    tags=["goal_tasks"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{goal_id}", status_code=status.HTTP_200_OK)
def read_all_goal_tasks(user: user_dependency, db: db_dependency, goal_id: int):
    try:
        if user is None:
            raise HTTPException(status_code=404, detail="認証に失敗しました")
        goal_tasks = db.query(GoalsTasks).filter(GoalsTasks.goal_id == goal_id).all()

        if not goal_tasks:
            raise HTTPException(status_code=404, detail='目標達成タスクが見つかりません')

        return {"detail": "目標達成タスクを取得しました", "goal_tasks": goal_tasks}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが取得できません")


@router.delete("/{goal_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal_tasks(user: user_dependency, db: db_dependency, goal_task_id: int):
    try:
        goal_task_repository = GoalTaskRepository()
        if user is None:
            raise HTTPException(status_code=404, detail="認証に失敗しました")
        goal_task = db.query(GoalsTasks).filter(GoalsTasks.goal_task_id == goal_task_id).first()

        if goal_task is None:
            raise HTTPException(status_code=404, detail='目標達成タスクが見つかりません')

        goal_task_repository.delete_goal_task_from_db(db, goal_task, commit=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが削除できません")


@router.put("/{goal_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_goal_task_status(user: user_dependency, db: db_dependency, goal_task_id: int,
                            new_status: GoalsTasksStatusEnum):
    try:
        if user is None:
            raise HTTPException(status_code=404, detail="認証に失敗しました")

        # リポジトリ呼び出し
        goal_task_repository = GoalTaskRepository()
        updated_task = goal_task_repository.update_goal_task_status_from_db(
            db, goal_task_id, new_status, commit=True
        )

        if updated_task is None:
            raise HTTPException(status_code=404, detail="目標達成タスクが見つかりません")
    except HTTPException:
        raise
    except (ValueError, GoalTaskNotFound, StatusUnchangedError, DataError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが更新できません")


@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_chat_reply(payload: GoalRequestWithTasks, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=404, detail="userが見つかりません")

        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        goal = payload.goal

        goal_tasks = payload.goal_tasks_list or []
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
            - goal_task_name: 50字以内のタスク名(参考書に関するアドバイスも付け加える)
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
              "goal_task_name": "基本情報技術者試験の1問1答をする",
              "deadline": "2025-09-11",
              "estimated_time": 25
            }},{{
              "goal_task_name": "基本情報技術者試験の1問1答をする",
              "deadline": "2025-09-11",
              "estimated_time": 35
            }},
            {{
              "goal_task_name": "基本情報技術者試験の過去問を解く",
              "deadline": "2025-09-12",
              "estimated_time": 90
            }}
          ]
        }}
            注意事項
            - 優先度は内部的に考慮するが、出力フィールドには含めない
            - タスクは優先度が高い順に締め切りを早く設定して
            - 長時間の作業は分割して複数タスクにする
            - 1日に複数タスクを含めてもよいが、それらのタスクを合計して平日は平日可用時間と休日は休日の可用時間内に収める
            - 現実的な時間配分を守る
            - 生成条件が与えられない場合は無視してよい
            - 注意: daily_schedule は無視してください
            -{json.dumps(goal_tasks, ensure_ascii=False)}は完了済みの目標達成タスクリストです。これらのタスクを考慮して不要な目標に向けた達成タスクは生成しない。
            この{json.dumps(goal_tasks, ensure_ascii=False)}は存在しない可能性もある。その場合は考慮しなくていい。
            """
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

        return {"detail": "目標達成タスクを生成しました", "goal_tasks": goal_tasks, "goal": goal}
    
    except HTTPException:
        raise
    except (ValueError, IntegrityError, DataError, GoalTaskNotFound, StatusUnchangedError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: タスクの生成に失敗しました")


@router.post("/save", status_code=status.HTTP_201_CREATED)
def save_goals_and_goal_tasks_and(user: user_dependency, payload: SaveRequest,
                                  db: Session = Depends(get_db)):
    try:
        if user is None:
            raise HTTPException(status_code=404, detail="認証に失敗しました")
        goal_repository = GoalRepository()
        goal = payload.goal
        goal_task_list = payload.goal_tasks
        goal_data = goal.model_dump()

        goal_data["status"] = GoalsStatusEnum.Unachieved.value

        goal_obj = Goals(**goal_data, user_id=user.get("user_id"))
        goal_obj.total_estimated_time = goal_obj.calculate_total_estimated_time()
        goal_repository.register_goal(db, goal_obj, commit=True)

        goal_task_repository = GoalTaskRepository()
        goal_task_items = []
        for goal_task in goal_task_list:
            goal_task_items.append(GoalsTasks(**goal_task.model_dump(), goal_id=goal_obj.goal_id))
        goal_task_repository.register_goal_task(db, goal_task_items, commit=True)
        return {
            "detail": "達成目標と目標達成タスクが保存されました",
            "goal_id": goal_obj.goal_id
        }
    except HTTPException:
        raise
    except (ValueError, IntegrityError, StatementError, DataError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが登録されません")