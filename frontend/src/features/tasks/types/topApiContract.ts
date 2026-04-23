export type TopApiGoalContract = {
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
  task_creation_rule: string | null;
};

export type TopApiGoalTaskContract = {
  goal_task_id: number;
  goal_id: number;
  order_num: number;
  goal_task_name: string;
  goal_task_status: string;
  deadline: string;
  estimated_time: number;
};

export type TopApiContract = {
  username: string;
  email: string;
  user_rank: string;
  user_points: number;
  goal?: TopApiGoalContract | null;
  goal_tasks?: TopApiGoalTaskContract[];
};