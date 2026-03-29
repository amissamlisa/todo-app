import type { Cards } from "./cards";

export type KanbanBoardProps = {
  TodoItems?: Cards[];
  isAddTaskEnabled?: boolean;
  onPointsChange?: (points: number) => void;
  onDoneTasksChange?: (todoItems: Cards[], inProgressItems: Cards[], doneItems: Cards[]) => void;
  onTodayTasksChange?: (todoItems: Cards[], inProgressItems: Cards[]) => void;
  onDeleteTasks?: (goal_task_id: number) => void;
};