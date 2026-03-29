import type { AxiosInstance } from "axios";
import type {
  GenerateGoalTasksPayload,
  GenerateGoalTasksResponse,
  SaveOrUpdateGoalTasksPayload,
} from "../types/goalTasksApi";

export const generateGoalTasks = async (
  api: AxiosInstance,
  payload: GenerateGoalTasksPayload
): Promise<GenerateGoalTasksResponse> => {
  const response = await api.post<GenerateGoalTasksResponse>("/goal_tasks/generate", payload);
  return response.data;
};

export const saveGoalTasks = async (
  api: AxiosInstance,
  payload: SaveOrUpdateGoalTasksPayload
): Promise<void> => {
  await api.post("/goal_tasks/save", payload);
};

export const updateGoalTasks = async (
  api: AxiosInstance,
  payload: SaveOrUpdateGoalTasksPayload
): Promise<void> => {
  await api.put("/goal_tasks/update", payload);
};
