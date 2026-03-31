import type { GoalPayload, GoalTask } from "./goalTasksApi";

export type TaskRegistrationCompleteState = {
  goal: GoalPayload;
  goalTasks: GoalTask[];
  goalTotalEstimatedTime?: number;
};
