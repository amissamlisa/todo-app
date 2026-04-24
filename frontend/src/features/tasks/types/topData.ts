import type { Rank } from "./rank";
import type { TopGoalTask } from "./topGaolTask";
import type { TopGoal } from "./topGoal";

export type TopData = {
  username: string;
  email: string;
  userRank: Rank;
  userPoints: number;
  goal: TopGoal | null;
  goalTasks: TopGoalTask[];
};