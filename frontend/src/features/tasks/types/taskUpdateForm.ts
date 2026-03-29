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
  goal_task_name: string;
  deadline: string;
  estimated_time: number;
};

export type TaskUpdateLocationState = {
  goalName?: string;
  completedGoalTasks?: CompletedGoalTask[];
};
