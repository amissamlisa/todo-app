export type TaskUpdateFormType = {
  goal: string;
  currentStatus: string;
  startDate: string;
  endDate: string;
  weekdayHours: string;
  holidayHours: string;
  conditions: string;
};

export type CompletedGoalTask = {
  goalTaskName: string;
  deadline: string;
  estimatedTime: number;
};

export type TaskUpdateLocationState = {
  goalName?: string;
  completedGoalTasks?: CompletedGoalTask[];
};
