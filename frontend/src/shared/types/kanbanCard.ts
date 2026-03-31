export type KanbanCardProps = {
  goalTaskId: number;
  goalTask: string;
  time: number;
  index: number;
  parent: string;
  deadline: string;
  onDeleteTask?: (goalTaskId: number) => void;
  onTaskEdit?: (goalTaskId: number, goalTaskName: string, estimatedTime: string, deadline: string) => void;
};