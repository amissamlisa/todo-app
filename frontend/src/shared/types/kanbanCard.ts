export type KanbanCardProps = {
  goal_task_id: number;
  goal_task: string;
  time: number;
  index: number;
  parent: string;
  deadline: string;
  onDeleteTask?: (goal_task_id: number) => void;
  onTaskEdit?: (goal_task_id: number, goal_task_name: string, estimated_time: string, deadline: string) => void;
};