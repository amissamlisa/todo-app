from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.schemas import GoalsTasksRequest, GoalsTasksOut
from ..models.models import Goals, GoalsTasks, GoalsTasksStatusEnum
from openai import OpenAI
import os
import json
from ..repository.repository import GoalTaskRepository, GoalRepository
from .auth import get_current_user

router = APIRouter(
    prefix="/goal_tasks",
    tags=["goal_tasks"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{goal_task_id}", status_code=status.HTTP_200_OK)
def read_goal_tasks(user: user_dependency, db: db_dependency, goal_task_id: int):
    if user is None:
        raise HTTPException(status_code=404, detail="認証に失敗")
    goal_tasks = db.query(GoalsTasks).filter(GoalsTasks.goal_task_id == goal_task_id).all()

    if goal_tasks is not None:
        return goal_tasks

    raise HTTPException(status_code=404, detail='目標達成タスクが見つかりません')


@router.delete("/{goal_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal_tasks(user: user_dependency, db: db_dependency, goal_task_id: int):
    goal_task_repository = GoalTaskRepository()
    if user is None:
        raise HTTPException(status_code=404, detail="認証に失敗")
    goal_task = db.query(GoalsTasks).filter(GoalsTasks.goal_task_id == goal_task_id).first()

    if goal_task is None:
        raise HTTPException(status_code=404, detail='目標達成タスクが見つかりません')

    goal_task_repository.delete_goal_task_from_db(db, goal_task, commit=True)


@router.put("/{goal_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_goal_task_status(user: user_dependency, db: db_dependency, goal_task_id: int,
                            new_status: GoalsTasksStatusEnum):
    goal_task_repository = GoalTaskRepository()
    if user is None:
        raise HTTPException(status_code=404, detail="認証に失敗")

    # リポジトリ呼び出し
    goal_task_repository = GoalTaskRepository()
    updated_task = goal_task_repository.update_goal_task_status_from_db(
        db, goal_task_id, new_status, commit=True
    )
    # print(updated_task.goal_task_status)

    if updated_task is None:
        raise HTTPException(status_code=404, detail="目標達成タスクが見つかりません")

    return {"message": "ステータスを更新しました"}


# stringstri123@A


def generate_chat_reply(goal: GoalsTasksRequest):
    try:
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

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
            - 平日可用時間(1日あたり) {goal.weekday_available_hours}
            - 休日の可用時間(1日あたり 祝日法第3条第3項による休日も含める) {goal.weekends_available_hours}
            - 生成条件（省略される場合あり） {goal.task_creation_rule}


            出力形式（JSON）
            - goal_tasks: タスク一覧（タスクの締め切りが早い順に並べる）
            - goal_task_name: 50字以内のタスク名(参考書に関するアドバイスも付け加える)
            - deadline: date型 (YYYY-MM-DD)(開始日と期限日・平日可用時間と休日の可用時間を考慮して)
            - estimated_time: 実行時間(1日の平日可用時間もしくは休日の可用時間を合計で下回るか、それらの可用時間と同じになるように決めて)

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
            }}
            {{
              "goal_task_name": "基本情報技術者試験の過去問を解く",
              "deadline": "2025-09-12",
              "estimated_time": 90
            }}
          ]
        }}
            注意事項
            - 優先度は内部的に考慮するが、出力フィールドには含めない
            - 長時間の作業は分割して複数タスクにする
            - 1日に複数タスクがあってもよいが、平日は平日可用時間と休日は休日の可用時間内に収める
            - 現実的な時間配分を守る
            - 生成条件が与えられない場合は無視してよい
            - 注意: daily_schedule は無視してください
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

        return goal_tasks

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
def save_goal_and_goals_tasks(user: user_dependency, goal_tasks_request: GoalsTasksRequest,
                              db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="goalが見つかりません")
    try:
        goal_repository = GoalRepository()
        goal_task_repository = GoalTaskRepository()
        goal = Goals(goal_name=goal_tasks_request.goal_name,
                     status_against_goal=goal_tasks_request.status_against_goal,
                     start_day=goal_tasks_request.start_day,
                     target_day=goal_tasks_request.target_day,
                     weekday_available_hours=goal_tasks_request.weekday_available_hours,
                     weekends_available_hours=goal_tasks_request.weekends_available_hours,
                     task_creation_rule=goal_tasks_request.task_creation_rule,
                     user_id=user.get('user_id'))

        goal_task_list_value = generate_chat_reply(goal)
        goal.total_estimated_time = goal.calculate_total_estimated_time()
        goal_data = goal_repository.register_goal(db, goal)

        for goal_task in goal_task_list_value:
            goal_task_item = GoalsTasks(goal_task_name=goal_task.goal_task_name, deadline=goal_task.deadline,
                                        estimated_time=goal_task.estimated_time,
                                        goal_id=goal_data.goal_id)
            try:
                goal_task_repository.register_goal_task(db, goal_task_item)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e, "データが登録されません"))
        return {
            "status": "ok",
            "message": "達成目標と目標達成タスクが保存されました",
            "goal_id": goal_data.goal_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
