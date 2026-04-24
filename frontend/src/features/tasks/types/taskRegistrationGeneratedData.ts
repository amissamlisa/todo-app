import type { GenerateGoalTasksResponse } from "./goalTasksApi";
import type { TaskRegistrationFormType } from "./taskRegistrationForm";

export type TaskRegistrationGeneratedData = {
  form?: TaskRegistrationFormType;
  generated?: GenerateGoalTasksResponse;
};
