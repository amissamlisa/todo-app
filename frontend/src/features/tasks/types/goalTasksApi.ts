export type GoalTask = {
  goalTaskName: string;
  deadline: string;
  estimatedTime: number;
};

export type GoalPayload = {
  goalName: string;
  statusAgainstGoal: string;
  startDay: string;
  targetDay: string;
  weekdayAvailableTime: number;
  weekendsAvailableTime: number;
  taskCreationRule?: string;
};

export type GenerateGoalTasksPayload = {
  goal: GoalPayload;
  completedGoalTasksList?: GoalTask[];
};

export type SaveOrUpdateGoalTasksPayload = {
  goal: GoalPayload;
  goalTasks: GoalTask[];
  goalTotalEstimatedTime: number;
};

export type GenerateGoalTasksResponse = {
  goalTasks: GoalTask[];
};
