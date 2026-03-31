import type { AxiosInstance } from "axios";
import type { Cards } from "../types/cards";
import type {
  ApiCreateGoalTaskPayload,
  ApiCreateGoalTaskResponse,
  ApiGoalTaskOrderPayload,
  ApiGoalTaskStatusPayload,
  ApiUpdateGoalTaskPayload,
  CreateGoalTaskPayload,
  GoalTaskOrderPayload,
  GoalTaskStatusPayload,
  UpdateGoalTaskPayload,
} from "../types/kanbanApi";

export const reorderGoalTasks = async (
  api: AxiosInstance,
  payload: GoalTaskOrderPayload
): Promise<void> => {
  const apiPayload: ApiGoalTaskOrderPayload = {
    from_goal_task_id: payload.fromGoalTaskId,
    to_goal_task_id: payload.toGoalTaskId,
    from_goal_task_order: payload.fromGoalTaskOrder,
    to_goal_task_order: payload.toGoalTaskOrder,
  };

  await api.put("/goal_tasks/order", apiPayload);
};

export const updateGoalTaskStatus = async (
  api: AxiosInstance,
  goalTaskId: number,
  payload: GoalTaskStatusPayload
): Promise<void> => {
  const apiPayload: ApiGoalTaskStatusPayload = {
    order_num: payload.orderNum,
    new_status: payload.newStatus,
  };

  await api.put(`/goal_tasks/status/${goalTaskId}`, apiPayload);
};

export const createGoalTask = async (
  api: AxiosInstance,
  payload: CreateGoalTaskPayload
): Promise<Cards | null> => {
  const apiPayload: ApiCreateGoalTaskPayload = {
    goal_task_name: payload.goalTask,
    estimated_time: payload.estimatedTime,
    deadline: payload.deadline,
    goal_task_status: payload.goalTaskStatus,
  };

  const response = await api.post<ApiCreateGoalTaskResponse>("/goal_tasks", apiPayload);
  const createdTask = response.data.goal_task;

  if (!createdTask) {
    return null;
  }

  return {
    goalTaskId: createdTask.goal_task_id,
    orderNum: createdTask.order_num,
    goalTaskStatus: createdTask.goal_task_status,
    goalTask: createdTask.goal_task_name,
    time: createdTask.estimated_time,
    deadline: createdTask.deadline,
  };
};

export const deleteGoalTask = async (
  api: AxiosInstance,
  goalTaskId: number
): Promise<void> => {
  await api.delete(`/goal_tasks/${goalTaskId}`);
};

export const updateGoalTask = async (
  api: AxiosInstance,
  goalTaskId: number,
  payload: UpdateGoalTaskPayload
): Promise<void> => {
  const apiPayload: ApiUpdateGoalTaskPayload = {
    goal_task_name: payload.goalTask,
    estimated_time: payload.estimatedTime,
    deadline: payload.deadline,
  };

  await api.put(`/goal_tasks/${goalTaskId}`, apiPayload);
};