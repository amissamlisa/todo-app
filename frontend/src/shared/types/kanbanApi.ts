export type GoalTaskOrderPayload = {
  fromGoalTaskId: number;
  toGoalTaskId: number;
  fromGoalTaskOrder: number;
  toGoalTaskOrder: number;
};

export type GoalTaskStatusPayload = {
  goalTaskId: number;
  orderNum: number;
  newStatus: string;
};

export type CreateGoalTaskPayload = {
  goalTask: string;
  estimatedTime: number;
  deadline: string;
  goalTaskStatus: string;
};

export type UpdateGoalTaskPayload = {
  goalTask: string;
  estimatedTime: number;
  deadline: string;
};

export type ApiGoalTaskOrderPayload = {
  from_goal_task_id: number;
  to_goal_task_id: number;
  from_goal_task_order: number;
  to_goal_task_order: number;
};

export type ApiGoalTaskStatusPayload = {
  order_num: number;
  new_status: string;
};

export type ApiCreateGoalTaskPayload = {
  goal_task_name: string;
  estimated_time: number;
  deadline: string;
  goal_task_status: string;
};

export type ApiUpdateGoalTaskPayload = {
  goal_task_name: string;
  estimated_time: number;
  deadline: string;
};

export type ApiCreateGoalTaskResponse = {
  goal_task?: {
    goal_task_id: number;
    goal_id: number;
    order_num: number;
    goal_task_status: string;
    goal_task_name: string;
    estimated_time: number;
    deadline: string;
  };
};