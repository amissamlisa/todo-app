from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from schemas import GoalsTasksRequest, GoalsTasksOut
from ..models import Goals
from openai import OpenAI
import os
import json
from ..repository.todo_repository import registerGoalAndGoalTasks

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@router.get("/goal-tasks-registration")
def goal_tasks_registration():
    return {"message": "Goal tasks registrationエンドポイントはまだ実装されていない"}    
@router.get("/goal-tasks-confirmation")
def goal_tasks_confirmation():
    return {"message": "Goal tasks confirmationはまだ実装されていない"}

@router.get("/tasks")
def get_tasks():
    return []

@router.post("/goal-tasks-preview")
def generate_chat_reply(goalTasksRequest: GoalsTasksRequest,status_code=status.HTTP_201_CREATED):
    goal = Goals(**goalTasksRequest.model_dump())
    print(goal)
    try:
        client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
        )

        response = client.response.create(
            model="gpt-4.1-nano",
            instructions="""あなたは目標達成のためのタスク設計コーチです。
            以下の入力（目標名／現在の状況／開始日／期限日／平日・休日の可用時間／生成条件）に基づき,
            現実的で実行可能なタスク群と日別配分案を作成してください。""",
            input=f"""入力
            - 目標名 {goal.goal_name}
            - 現在の状況 {goal.status_against_goal}
            - 開始日 {goal.start_date}
            - 期限日 {goal.target_date}
            - 平日可用時間 {goal.weekday_available_hours}
            - 休日の可用時間 {goal.weekends_available_hours}
            - 生成条件（省略される場合あり） {goal.task_creation_rule}


            出力形式（JSON）
            - tasks: タスク一覧（優先度の高い順に並べる）
            - goal_task_name: 50字以内のタスク名
            - deadline: date型 (YYYY-MM-DD)
            - estimated_time: 実行時間（0.5〜3.0h）

            出力例
            {
                "tasks": [
                    {
                    "goal_task_name": "基本情報技術者試験の動画視聴をする",
                    "deadline": "2025-09-10",
                    "estimated_time": 2.0
                    },
                    {
                    "goal_task_name": "基本情報技術者試験の過去問を解く",
                    "deadline": "2025-09-12",
                    "estimated_time": 2.5
                    }
                ]
            }
            注意事項
            - 優先度は内部的に考慮するが、出力フィールドには含めない
            - 長時間の作業は分割して複数タスクにする
            - 現実的な時間配分を守る
            - 生成条件が与えられない場合は無視してよい"""
        )
        tasks_json = json.loads(response.output_text)
        goal_tasks = []
        for task in tasks_json["tasks"]:
            goal_tasks.append(GoalsTasksOut(**task))
        return {"goal": goal, "tasks": tasks_json["tasks"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

@router.post("/goal-tasks",status_code=status.HTTP_201_CREATED)
def save_goal_tasks(goalTasksRequest: GoalsTasksRequest,db: Session = Depends(get_db)):
    result = generate_chat_reply(goalTasksRequest)
    goal = result.get('goal')
    goal_tasks = result.get('tasks')
    if goal is None or goal_tasks is None:
        raise HTTPException(status_code=500, detail="達成目標と目標達成タスクが設定されていません")
    response = registerGoalAndGoalTasks(db, goal, goal_tasks)
    return response