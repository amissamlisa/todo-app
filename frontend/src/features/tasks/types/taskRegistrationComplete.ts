import type { GoalPayload, GoalTask } from "./goalTasksApi";

export type TaskRegistrationCompleteState = {
  goal: GoalPayload;
  goal_tasks: GoalTask[];
  goal_total_estimated_time?: number;
};
