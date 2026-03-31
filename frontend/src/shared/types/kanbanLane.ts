import type { Cards } from "./cards";

export type UseKanbanLaneParams = {
  canAddTask: boolean;
  onAddTask?: (
    goalTaskName: string,
    estimatedTime: string,
    deadline: string
  ) => Promise<boolean>;
};

export type KanbanLaneProps = {
  title: string;
  items: Cards[];
  bgColor: string;
  canAddTask?: boolean;
  onDeleteTasks?: (goalTaskId: number) => void;
  onEditTasks?: (goalTaskId: number, goalTaskName: string, estimatedTime: string, deadline: string) => void;
  onAddTask?: (goalTaskName: string, estimatedTime: string, deadline: string) => Promise<boolean>;
};
