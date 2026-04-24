export type Cards = {
  goalTaskId: number;
  orderNum: number;
  goalTaskStatus: string;
  goalTask: string;
  time: number;
  deadline: string;
  onDeleteTask?: (goalTaskId: number) => void;
};