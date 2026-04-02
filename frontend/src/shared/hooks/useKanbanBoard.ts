import { type DragEndEvent, type DragStartEvent } from "@dnd-kit/core";
import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { useAuth } from "../../features/users/auth/useAuth";
import {
  createGoalTask,
  reorderGoalTasks,
  updateGoalTaskStatus,
} from "../api/kanbanApi";
import type { Cards } from "../types/cards";
import type { ActiveCard, KanbanBoardProps } from "../types/kanbanBoard";

const splitByStatus = (items: Cards[]) => ({
  todo: items.filter((item) => item.goalTaskStatus === "未着手"),
  inProgress: items.filter((item) => item.goalTaskStatus === "作業中"),
  done: items.filter((item) => item.goalTaskStatus === "完了"),
});

export const useKanbanBoard = ({
  TodoItems,
  onPointsChange,
  onDoneTasksChange,
  onTodayTasksChange,
  onDeleteTasks,
}: KanbanBoardProps) => {
  const { token, api } = useAuth();
  const initial = splitByStatus(TodoItems ?? []);
  const [todoItems, setTodoItems] = useState<Array<Cards>>(() => initial.todo);
  const [doneItems, setDoneItems] = useState<Array<Cards>>(() => initial.done);
  const [inProgressItems, setInProgressItems] = useState<Array<Cards>>(
    () => initial.inProgress
  );
  const [activeCard, setActiveCard] = useState<ActiveCard | null>(null);
  const previousDoneCountRef = useRef(initial.done.length);

  useEffect(() => {
    if (!onPointsChange) return;
    const gainedPoints = doneItems.length - previousDoneCountRef.current;
    previousDoneCountRef.current = doneItems.length;

    if (gainedPoints > 0) {
      onPointsChange(gainedPoints);
    }
  }, [doneItems, onPointsChange]);

  useEffect(() => {
    if (!onDoneTasksChange) return;
    onDoneTasksChange(todoItems, inProgressItems, doneItems);
  }, [todoItems, inProgressItems, doneItems, onDoneTasksChange]);

  useEffect(() => {
    if (!onTodayTasksChange) return;
    onTodayTasksChange(todoItems, inProgressItems);
  }, [todoItems, inProgressItems, onTodayTasksChange]);

  const formatDateForDisplay = (value: string) => value.replace(/-/g, "/");

  const getListByLane = (lane: string) => {
    switch (lane) {
      case "未着手":
        return todoItems;
      case "作業中":
        return inProgressItems;
      case "完了":
        return doneItems;
      default:
        return todoItems;
    }
  };

  const setListByLane = (lane: string, items: Cards[]) => {
    switch (lane) {
      case "未着手":
        setTodoItems(items);
        break;
      case "作業中":
        setInProgressItems(items);
        break;
      case "完了":
        setDoneItems(items);
        break;
      default:
        setTodoItems(items);
    }
  };

  const moveItemWithinLane = (items: Cards[], fromIndex: number, toIndex: number) => {
    if (fromIndex === toIndex) return items;
    const next = [...items];
    const [moved] = next.splice(fromIndex, 1);
    next.splice(toIndex, 0, moved);
    return next;
  };

  const syncGoalTaskOrder = async (items: Cards[], fromIndex: number, toIndex: number) => {
    const fromTask = items[fromIndex];
    const toTask = items[toIndex];
    if (!fromTask || !toTask || !token) return;

    try {
      await reorderGoalTasks(api, {
        fromGoalTaskId: fromTask.goalTaskId,
        toGoalTaskId: toTask.goalTaskId,
        fromGoalTaskOrder: fromTask.orderNum,
        toGoalTaskOrder: toTask.orderNum,
      });
    } catch (err) {
      console.error("updateGoalTaskOrder failed", err);
    }
  };

  const syncGoalTaskStatus = async (
    goalTaskId: number,
    orderNum: number,
    goalTaskStatus: string
  ) => {
    try {
      await updateGoalTaskStatus(api, goalTaskId, {
        goalTaskId: goalTaskId,
        orderNum: orderNum,
        newStatus: goalTaskStatus,
      });
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.error("updateGoalTaskStatusAndOrder failed", {
          status: err.response?.status,
          method: err.config?.method,
          url: err.config?.url,
          response: err.response?.data,
        });
      } else {
        console.error("updateGoalTaskStatusAndOrder failed", err);
      }
    }
  };

  const handleDeleteTask = (goalTaskId: number) => {
    setTodoItems((previous) => previous.filter((task) => task.goalTaskId !== goalTaskId));
    setInProgressItems((previous) => previous.filter((task) => task.goalTaskId !== goalTaskId));
    setDoneItems((previous) => previous.filter((task) => task.goalTaskId !== goalTaskId));
    onDeleteTasks?.(goalTaskId);
  };

  const handleEditTask = (
    goalTaskId: number,
    goalTaskName: string,
    estimatedTime: string,
    deadline: string
  ) => {
    const nextEstimatedTime = Number(estimatedTime);
    const updateCard = (task: Cards) => {
      if (task.goalTaskId !== goalTaskId) return task;
      return {
        ...task,
        goalTask: goalTaskName,
        time: Number.isNaN(nextEstimatedTime) ? task.time : nextEstimatedTime,
        deadline,
      };
    };

    setTodoItems((previous) => previous.map(updateCard));
    setInProgressItems((previous) => previous.map(updateCard));
    setDoneItems((previous) => previous.map(updateCard));
  };

  const handleAddTask = async (
    lane: string,
    goalTaskName: string,
    estimatedTime: string,
    deadline: string
  ) => {
    if (!goalTaskName.trim() || !estimatedTime.trim() || !deadline.trim() || !token) {
      return false;
    }

    const nextEstimatedTime = Number(estimatedTime);
    if (Number.isNaN(nextEstimatedTime) || nextEstimatedTime <= 0) {
      return false;
    }

    const normalizedDeadline = deadline.replace(/\//g, "-");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(normalizedDeadline)) {
      return false;
    }

    const payload = {
      goalTask: goalTaskName,
      estimatedTime: nextEstimatedTime,
      deadline: normalizedDeadline,
      goalTaskStatus: lane,
    };

    try {
      const newTask = await createGoalTask(api, payload);
      if (!newTask) {
        return false;
      }

      const currentLaneItems = getListByLane(lane);
      setListByLane(lane, [...currentLaneItems, newTask]);
      return true;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.error("createGoalTask failed", {
          status: err.response?.status,
          method: err.config?.method,
          url: err.config?.url,
          response: err.response?.data,
          payload,
        });
      } else {
        console.error("createGoalTask failed", err);
      }
      return false;
    }
  };

  const handleDragStart = (event: DragStartEvent) => {
    const current = event.active.data.current;
    if (!current) return;

    setActiveCard({
      goalTaskId: current.goalTaskId,
      goalTask: current.goalTask,
      time: current.time,
      deadline: current.deadline,
    });
  };

  const handleDragEnd = (event: DragEndEvent) => {
    setActiveCard(null);
    const overLane = event.over?.data.current?.lane ?? event.over?.id;
    if (!overLane) return;
    const container = String(overLane).startsWith("lane-")
      ? String(overLane).replace("lane-", "")
      : String(overLane);
    const index = event.active.data.current?.index ?? 0;
    const parent = event.active.data.current?.parent ?? "未着手";

    if (parent === container) {
      const overIndex = event.over?.data.current?.index;
      if (overIndex === undefined || overIndex === index) return;

      const currentList = getListByLane(parent);
      void syncGoalTaskOrder(currentList, index, overIndex);
      const reordered = moveItemWithinLane(currentList, index, overIndex);
      setListByLane(parent, reordered);
      return;
    }

    const fromList = getListByLane(parent);
    const toList = getListByLane(container);
    const moving = fromList[index];
    if (!moving) return;

    const updatedFrom = fromList.filter((_, itemIndex) => itemIndex !== index);
    const updatedTo = [...toList, moving];

    setListByLane(parent, updatedFrom);
    setListByLane(container, updatedTo);
    void syncGoalTaskStatus(moving.goalTaskId, toList.length + 1, container);
  };

  const handleDragCancel = () => {
    setActiveCard(null);
  };

  return {
    todoItems,
    inProgressItems,
    doneItems,
    activeCard,
    formatDateForDisplay,
    handleDeleteTask,
    handleEditTask,
    handleAddTask,
    handleDragStart,
    handleDragEnd,
    handleDragCancel,
  };
};