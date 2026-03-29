import type { Cards } from "./cards";

export type KanbanLaneProps = {
  title: string;
  items: Cards[];
  bgColor: string;
  isAddTaskEnabled?: boolean;
  onDeleteTasks?: (goal_task_id: number) => void;
  onEditTasks?: (goal_task_id: number, goal_task_name: string, estimated_time: string, deadline: string) => void;
  onAddTask?: (goal_task_name: string, estimated_time: string, deadline: string) => Promise<boolean>;
};
