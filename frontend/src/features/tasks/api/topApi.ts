import type { AxiosInstance } from "axios";
import type { TopData } from "../types/topData";
import type { TopApiContract } from "../types/topApiContract";

export const fetchTopData = async (api: AxiosInstance): Promise<TopData> => {
  const response = await api.get<TopApiContract>("/top");
  const data = response.data;

  const goal = data.goal
    ? {
      goalId: data.goal.goal_id,
      userId: data.goal.user_id,
      goalName: data.goal.goal_name,
      status: data.goal.status,
      startDay: data.goal.start_day,
      targetDay: data.goal.target_day,
      statusAgainstGoal: data.goal.status_against_goal,
      weekdayAvailableTime: data.goal.weekday_available_time,
      weekendsAvailableTime: data.goal.weekends_available_time,
      totalEstimatedTime: data.goal.total_estimated_time,
      taskCreationRule: data.goal.task_creation_rule,
    }
    : null;

  const goalTasks = (data.goal_tasks ?? []).map((task) => ({
    goalTaskId: task.goal_task_id,
    goalId: task.goal_id,
    orderNum: task.order_num,
    goalTaskName: task.goal_task_name,
    goalTaskStatus: task.goal_task_status,
    deadline: task.deadline,
    estimatedTime: task.estimated_time,
  }));

  return {
    username: data.username,
    email: data.email,
    userRank: data.user_rank,
    userPoints: data.user_points,
    goal,
    goalTasks,
  };
};

export const deleteGoal = async (api: AxiosInstance, goalId: number): Promise<void> => {
  await api.delete(`/goal/${goalId}`);
};

export const updateTopPoints = async (api: AxiosInstance, points: number): Promise<void> => {
  await api.put("/top/points", { points });
};

export const updateTopRank = async (api: AxiosInstance, userRank: string): Promise<void> => {
  await api.put("/top/rank", { user_rank: userRank });
};
