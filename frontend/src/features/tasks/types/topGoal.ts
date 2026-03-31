export type TopGoal = {
  goalId: number;
  userId: number;
  goalName: string;
  status: string;
  startDay: string;
  targetDay: string;
  statusAgainstGoal: string;
  weekdayAvailableTime: number;
  weekendsAvailableTime: number;
  totalEstimatedTime: number;
  taskCreationRule?: string | null;
};