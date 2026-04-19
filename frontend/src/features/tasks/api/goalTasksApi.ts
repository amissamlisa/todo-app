import type { AxiosInstance } from "axios";
import type {
  GoalTask,
  GenerateGoalTasksPayload,
  GenerateGoalTasksResponse,
  SaveOrUpdateGoalTasksPayload,
} from "../types/goalTasksApi";
import type {
  ApiGenerateGoalTasksPayload,
  ApiGenerateGoalTasksResponse,
  ApiGoalPayload,
  ApiGoalTask,
  ApiSaveOrUpdateGoalTasksPayload,
} from "../types/goalTasksApiContract.ts";

const toApiGoalTask = (task: GoalTask): ApiGoalTask => ({
  goal_task_name: task.goalTaskName,
  deadline: task.deadline,
  estimated_time: task.estimatedTime,
  goal_task_status: task.goalTaskStatus,
});

const toCamelGoalTask = (task: ApiGoalTask): GoalTask => ({
  goalTaskName: task.goal_task_name,
  deadline: task.deadline,
  estimatedTime: task.estimated_time,
});

const toApiGoalPayload = (goal: GenerateGoalTasksPayload["goal"]): ApiGoalPayload => ({
  goal_name: goal.goalName,
  status_against_goal: goal.statusAgainstGoal,
  start_day: goal.startDay,
  target_day: goal.targetDay,
  weekday_available_time: goal.weekdayAvailableTime,
  weekends_available_time: goal.weekendsAvailableTime,
  task_creation_rule: goal.taskCreationRule,
});

export const generateGoalTasks = async (
  api: AxiosInstance,
  payload: GenerateGoalTasksPayload
): Promise<GenerateGoalTasksResponse> => {
  const apiPayload: ApiGenerateGoalTasksPayload = {
    goal: toApiGoalPayload(payload.goal),
    completed_goal_tasks_list: payload.completedGoalTasksList?.map(toApiGoalTask),
  };
  const response = await api.post<ApiGenerateGoalTasksResponse>("/goal-tasks/generate", apiPayload);
  return {
    goalTasks: response.data.goal_tasks.map(toCamelGoalTask),
  };
};

export const saveGoalTasks = async (
  api: AxiosInstance,
  payload: SaveOrUpdateGoalTasksPayload
): Promise<void> => {
  const apiPayload: ApiSaveOrUpdateGoalTasksPayload = {
    goal: toApiGoalPayload(payload.goal),
    goal_tasks: payload.goalTasks.map(toApiGoalTask),
    goal_total_estimated_time: payload.goalTotalEstimatedTime,
  };
  await api.post("/goal/", apiPayload);
};

export const updateGoalTasks = async (
  api: AxiosInstance,
  payload: SaveOrUpdateGoalTasksPayload
): Promise<void> => {
  const apiPayload: ApiSaveOrUpdateGoalTasksPayload = {
    goal: toApiGoalPayload(payload.goal),
    goal_tasks: payload.goalTasks.map(toApiGoalTask),
    goal_total_estimated_time: payload.goalTotalEstimatedTime,
  };
  await api.put("/goal/", apiPayload);
};
