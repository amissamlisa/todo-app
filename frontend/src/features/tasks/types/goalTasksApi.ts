export type GoalTask = {
  goal_task_name: string;
  deadline: string;
  estimated_time: number;
};

export type GoalPayload = {
  goal_name: string;
  status_against_goal: string;
  start_day: string;
  target_day: string;
  weekday_available_time: number;
  weekends_available_time: number;
  task_creation_rule?: string;
};

export type GenerateGoalTasksPayload = {
  goal: GoalPayload;
  goal_tasks_list?: unknown[];
  completed_goal_tasks_list?: GoalTask[];
};

export type SaveOrUpdateGoalTasksPayload = {
  goal: GoalPayload;
  goal_tasks: GoalTask[];
  goal_total_estimated_time: number;
};

export type GenerateGoalTasksResponse = {
  goal_tasks?: GoalTask[];
};
