export type Cards = {
  goal_task_id: number;
  order_num: number;
  goal_task_status: string;
  goal_task: string;
  time: number;
  deadline: string;
  onDeleteTask?: (goal_task_id: number) => void;
};