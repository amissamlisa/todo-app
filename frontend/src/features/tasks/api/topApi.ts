import type { AxiosInstance } from "axios";
import type { TopData } from "../types/topData";
import type { TopApiResponse } from "../types/topAPIResponse";

export const fetchTopData = async (api: AxiosInstance): Promise<TopData> => {
  const response = await api.get<TopApiResponse>("/top");
  const data = response.data;

  return {
    username: data.username,
    email: data.email,
    userRank: data.user_rank,
    userPoints: data.user_points,
    goal: data.goal,
    goalTasks: data.goal_tasks ?? [],
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
