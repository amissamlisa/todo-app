export type TaskUpdateFormType = {
  goal: string;
  currentStatus: string;
  startDate: string;
  endDate: string;
  weekdayAvailableHours: string;
  holidayAvailableHours: string;
  conditions: string;
};

export type CompletedGoalTask = {
  goalTaskName: string;
  deadline: string;
  estimatedTime: number;
  goalTaskStatus: string;
};

export type TaskUpdateLocationState = {
  goalName?: string;
  completedGoalTasks?: CompletedGoalTask[];
  formValues?: TaskUpdateFormType;
};
