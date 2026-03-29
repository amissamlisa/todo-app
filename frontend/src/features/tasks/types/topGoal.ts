export type TopGoal = {
  goal_id: number;
  user_id: number;
  goal_name: string;
  status: string;
  start_day: string;
  target_day: string;
  status_against_goal: string;
  weekday_available_time: number;
  weekends_available_time: number;
  total_estimated_time: number;
  task_creation_rule?: string | null;
};