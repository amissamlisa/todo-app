import type { GenerateGoalTasksResponse } from "./goalTasksApi";
import type { CompletedGoalTask, TaskUpdateFormType } from "./taskUpdateForm";

export type TaskUpdateGeneratedData = {
  form?: TaskUpdateFormType;
  generated?: GenerateGoalTasksResponse;
  goalName?: string;
  completedGoalTasks?: CompletedGoalTask[];
};
