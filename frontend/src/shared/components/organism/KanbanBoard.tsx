import { DndContext, DragOverlay, rectIntersection } from "@dnd-kit/core";
import { useEffect, useState } from "react";
import KanbanLane from "../molecules/KanbanLane";
import type { Cards } from "../../types/cards";
import { useAuth } from "../../../features/users/auth/useAuth";
import type { KanbanBoardProps } from "../../types/kanbanBoard";
import axios from "axios";

type ActiveCard = {
  goal_task_id: number;
  goal_task: string;
  time: number;
  deadline: string;
};

export default function KanbanBoard({ TodoItems, isAddTaskEnabled = true, onPointsChange, onDoneTasksChange, onTomorrowTasksChange, onDeleteTasks }: KanbanBoardProps) {
  const { token, api } = useAuth();

  const splitByStatus = (items: Cards[]) => ({
    todo: items.filter((item) => item.goal_task_status === "未着手"),
    inProgress: items.filter((item) => item.goal_task_status === "作業中"),
    done: items.filter((item) => item.goal_task_status === "完了"),
  });

  const initial = splitByStatus(TodoItems ?? []);
  const [todoItems, setTodoItems] = useState<Array<Cards>>(() => initial.todo);
  const [doneItems, setDoneItems] = useState<Array<Cards>>(() => initial.done);
  const [inProgressItems, setInProgressItems] = useState<Array<Cards>>(
    () => initial.inProgress
  );
  const [activeCard, setActiveCard] = useState<ActiveCard | null>(null);

  useEffect(() => {
    if (!onPointsChange) return;
    onPointsChange(doneItems.length);
  }, [doneItems, onPointsChange]);

  useEffect(() => {
    if (!onDoneTasksChange) return;
    onDoneTasksChange(todoItems, inProgressItems, doneItems);
  }, [todoItems, inProgressItems, doneItems, onDoneTasksChange]);

  useEffect(() => {
    if (!onTomorrowTasksChange) return;
    onTomorrowTasksChange(todoItems, inProgressItems);
  }, [todoItems, inProgressItems, onTomorrowTasksChange]);


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



  const updateGoalTaskOrder = async (items: Cards[], fromIndex: number, toIndex: number) => {
    const fromTask = items[fromIndex];
    const toTask = items[toIndex];
    if (!fromTask || !toTask || !token) return;

    const payload = {
      from_goal_task_id: fromTask.goal_task_id,
      to_goal_task_id: toTask.goal_task_id,
      from_goal_task_order: fromTask.order_num,
      to_goal_task_order: toTask.order_num,
    };

    try {
      await api.put(`/goal_tasks/order`, payload);
    } catch (error) {
      console.error("updateGoalTaskOrder failed", error);
    }
  };

  const updateGoalTaskStatusAndOrder = async (goal_task_id: number, order_num: number, goal_task_status: string) => {
    const payload = {
      goal_task_id: goal_task_id,
      order_num: order_num,
      new_status: goal_task_status,
    };

    try {
      await api.put(`/goal_tasks/status/${goal_task_id}`, payload);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("updateGoalTaskStatusAndOrder failed", {
          status: error.response?.status,
          method: error.config?.method,
          url: error.config?.url,
          response: error.response?.data,
          payload,
        });
      } else {
        console.error("updateGoalTaskStatusAndOrder failed", error);
      }
    }
  };

  const moveItemWithinLane = (items: Cards[], fromIndex: number, toIndex: number) => {
    if (fromIndex === toIndex) return items;
    const next = [...items];
    const [moved] = next.splice(fromIndex, 1);
    next.splice(toIndex, 0, moved);

    return next;
  };

  const handleDeleteTask = (goal_task_id: number) => {
    setTodoItems((previous) => previous.filter((task) => task.goal_task_id !== goal_task_id));
    setInProgressItems((previous) => previous.filter((task) => task.goal_task_id !== goal_task_id));
    setDoneItems((previous) => previous.filter((task) => task.goal_task_id !== goal_task_id));
    onDeleteTasks?.(goal_task_id);
  };

  const handleEditTask = (goal_task_id: number, goal_task_name: string, estimated_time: string, deadline: string) => {
    const nextEstimatedTime = Number(estimated_time);
    const updateCard = (task: Cards) => {
      if (task.goal_task_id !== goal_task_id) return task;
      return {
        ...task,
        goal_task: goal_task_name,
        time: Number.isNaN(nextEstimatedTime) ? task.time : nextEstimatedTime,
        deadline,
      };
    };

    setTodoItems((previous) => previous.map(updateCard));
    setInProgressItems((previous) => previous.map(updateCard));
    setDoneItems((previous) => previous.map(updateCard));
  };

  const handleAddTask = async (lane: string, goal_task_name: string, estimated_time: string, deadline: string) => {
    if (!goal_task_name.trim() || !estimated_time.trim() || !deadline.trim() || !token) {
      return false;
    }

    const nextEstimatedTime = Number(estimated_time);
    if (Number.isNaN(nextEstimatedTime) || nextEstimatedTime <= 0) {
      return false;
    }

    const normalizedDeadline = deadline.replace(/\//g, "-");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(normalizedDeadline)) {
      return false;
    }

    const payload = {
      goal_task_name,
      estimated_time: nextEstimatedTime,
      deadline: normalizedDeadline,
      goal_task_status: lane,
    };

    try {
      const response = await api.post(`/goal_tasks`, payload);

      const createdTask = response.data.goal_task;
      if (!createdTask) {
        return false;
      }

      const currentLaneItems = getListByLane(lane);
      const newTask: Cards = {
        goal_task_id: createdTask.goal_task_id,
        order_num: createdTask.order_num,
        goal_task_status: createdTask.goal_task_status,
        goal_task: createdTask.goal_task_name,
        time: createdTask.estimated_time,
        deadline: createdTask.deadline,
      };

      setListByLane(lane, [...currentLaneItems, newTask]);
      return true;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("createGoalTask failed", {
          status: error.response?.status,
          method: error.config?.method,
          url: error.config?.url,
          response: error.response?.data,
          payload,
        });
      } else {
        console.error("createGoalTask failed", error);
      }
      return false;
    }
  };



  return (
    <DndContext
      collisionDetection={rectIntersection}
      onDragStart={(e) => {
        const current = e.active.data.current;
        if (!current) return;

        setActiveCard({
          goal_task_id: current.goal_task_id,
          goal_task: current.goal_task,
          time: current.time,
          deadline: current.deadline,
        });
      }}
      onDragEnd={(e) => {
        setActiveCard(null);
        const overLane = e.over?.data.current?.lane ?? e.over?.id;
        if (!overLane) return;
        const container = String(overLane).startsWith("lane-")
          ? String(overLane).replace("lane-", "")
          : String(overLane);
        const index = e.active.data.current?.index ?? 0;
        const parent = e.active.data.current?.parent ?? "未着手";

        if (parent === container) {
          const overIndex = e.over?.data.current?.index;
          if (overIndex === undefined) return;
          if (overIndex === index) return;

          const currentList = getListByLane(parent);
          updateGoalTaskOrder(currentList, index, overIndex);
          const reordered = moveItemWithinLane(currentList, index, overIndex);
          setListByLane(parent, reordered);
          return;
        }

        const fromList = getListByLane(parent);
        const toList = getListByLane(container);
        const moving = fromList[index];
        if (!moving) return;

        const updatedFrom = fromList.filter((_, i) => i !== index);
        const updatedTo = [...toList, moving];

        setListByLane(parent, updatedFrom);
        setListByLane(container, updatedTo);
        updateGoalTaskStatusAndOrder(moving.goal_task_id, toList.length + 1, container);
      }}
      onDragCancel={() => {
        setActiveCard(null);
      }}
    >
      <div className="flex flex-col">
        <div className="flex flex-col">
          <KanbanLane title="未着手" items={todoItems} bgColor="#FF8E8E" isAddTaskEnabled={isAddTaskEnabled} onDeleteTasks={handleDeleteTask} onEditTasks={handleEditTask} onAddTask={(goal_task_name, estimated_time, deadline) => handleAddTask("未着手", goal_task_name, estimated_time, deadline)} />
          <KanbanLane title="作業中" items={inProgressItems} bgColor="#FFC68E" isAddTaskEnabled={isAddTaskEnabled} onDeleteTasks={handleDeleteTask} onEditTasks={handleEditTask} onAddTask={(goal_task_name, estimated_time, deadline) => handleAddTask("作業中", goal_task_name, estimated_time, deadline)} />
          <KanbanLane title="完了" items={doneItems} bgColor="#8EFF8E" isAddTaskEnabled={isAddTaskEnabled} onDeleteTasks={handleDeleteTask} onEditTasks={handleEditTask} onAddTask={(goal_task_name, estimated_time, deadline) => handleAddTask("完了", goal_task_name, estimated_time, deadline)} />
        </div>
      </div>
      <DragOverlay>
        {activeCard ? (
          <div className="p-3 m-2 bg-white rounded-lg border border-primary text-primary shadow-sm flex justify-between opacity-95 w-[clamp(120px,65vw,540px)]">
            <div>
              <p>{activeCard.deadline} {activeCard.time}分</p>
              <p>{activeCard.goal_task}</p>
            </div>
          </div>
        ) : null}
      </DragOverlay>
    </DndContext>
  );
}
