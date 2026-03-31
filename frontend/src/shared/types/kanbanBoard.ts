import type { Cards } from "./cards";

export type ActiveCard = {
  goalTaskId: number;
  goalTask: string;
  time: number;
  deadline: string;
};

export type KanbanBoardProps = {
  TodoItems?: Cards[];
  canAddTask?: boolean;
  onPointsChange?: (points: number) => void;
  onDoneTasksChange?: (todoItems: Cards[], inProgressItems: Cards[], doneItems: Cards[]) => void;
  onTodayTasksChange?: (todoItems: Cards[], inProgressItems: Cards[]) => void;
  onDeleteTasks?: (goalTaskId: number) => void;
};