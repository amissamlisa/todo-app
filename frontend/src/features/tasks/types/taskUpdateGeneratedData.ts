import type { GenerateGoalTasksResponse } from "./goalTasksApi";
import type { TaskUpdateFormType } from "./taskUpdateForm";

export type TaskUpdateGeneratedData = {
  form?: TaskUpdateFormType;
  generated?: GenerateGoalTasksResponse;
};
