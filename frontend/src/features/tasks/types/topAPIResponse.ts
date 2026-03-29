import type { TopData } from "./topData";

export type TopApiResponse = {
  username: string;
  email: string;
  user_rank: string;
  user_points: number;
  goal: TopData["goal"];
  goal_tasks?: TopData["goalTasks"];
};