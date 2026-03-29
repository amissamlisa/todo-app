import type { TopGoalTask } from "./topGaolTask";
import type { TopGoal } from "./topGoal";

export type TopData = {
  username: string;
  email: string;
  userRank: string;
  userPoints: number;
  goal: TopGoal | null;
  goalTasks: TopGoalTask[];
};