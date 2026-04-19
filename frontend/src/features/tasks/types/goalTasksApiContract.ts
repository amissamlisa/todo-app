export type ApiGoalTask = {
  goal_task_name: string;
  deadline: string;
  estimated_time: number;
  goal_task_status?: string;
};

export type ApiGoalPayload = {
  goal_name: string;
  status_against_goal: string;
  start_day: string;
  target_day: string;
  weekday_available_time: number;
  weekends_available_time: number;
  task_creation_rule?: string;
};

export type ApiGenerateGoalTasksPayload = {
  goal: ApiGoalPayload;
  completed_goal_tasks_list?: ApiGoalTask[];
};

export type ApiSaveOrUpdateGoalTasksPayload = {
  goal: ApiGoalPayload;
  goal_tasks: ApiGoalTask[];
  goal_total_estimated_time: number;
};

export type ApiGenerateGoalTasksResponse = {
  goal_tasks: ApiGoalTask[];
};