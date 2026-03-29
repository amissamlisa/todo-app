import { useDraggable, useDroppable } from "@dnd-kit/core";
import { CSS } from "@dnd-kit/utilities";
import { useAuth } from "../../../features/users/auth/useAuth";
import { useState } from "react";
import { TwoButtonModal } from "../molecules/TwoButtonModal";
import { BsThreeDots } from "react-icons/bs";
import { OperationModal } from "../molecules/OperationModal";
import { TaskConfigModal } from "../molecules/TaskConfigModal";
import type { KanbanCardProps } from "../../types/kanbanCard";
import axios from "axios";

export const KanbanCard = ({
  goal_task_id,
  goal_task,
  time,
  deadline,
  index,
  parent,
  onDeleteTask,
  onTaskEdit,
}: KanbanCardProps) => {
  const { api } = useAuth();
  const formatDateForDisplay = (value: string) => value.replace(/-/g, "/");
  const [activeModal, setActiveModal] = useState<
    "operation" | "delete" | "edit" | null
  >(null);
  const [editedTaskName, setEditedTaskName] = useState(goal_task);
  const [editedEstimatedTime, setEditedEstimatedTime] = useState(time.toString());
  const [editedDeadline, setEditedDeadline] = useState(formatDateForDisplay(deadline));
  const {
    attributes,
    listeners,
    setNodeRef: setDraggableRef,
    transform,
    isDragging,
  } = useDraggable({
    id: `goal_task_${goal_task_id}`,
    data: {
      goal_task_id,
      goal_task,
      time,
      index,
      parent,
      deadline,
    },
  });

  const { setNodeRef: setDroppableRef } = useDroppable({
    id: `goal_task_${goal_task_id}`,
    data: {
      lane: parent,
      index,
    },
  });

  const setNodeRef = (node: HTMLDivElement | null) => {
    setDraggableRef(node);
    setDroppableRef(node);
  };

  const deleteTaskById = async (goal_task_id: number) => {
    try {
      await api.delete(
        `/goal_tasks/${goal_task_id}`
      );
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.error("/goal_tasks/save error", err.response?.data);
        console.error(err.response?.data?.detail ?? "目標タスクの登録に失敗しました");
      } else {
        console.error("Unexpected error", err);
      }
    }
  };

  const editTaskById = async (goal_task_id: number, goal_task_name: string, estimated_time: string, deadline: string) => {
    try {
      const normalizedDeadline = deadline.replace(/\//g, "-");
      await api.put(
        `/goal_tasks/${goal_task_id}`,
        {
          goal_task_name: goal_task_name,
          estimated_time: Number(estimated_time),
          deadline: normalizedDeadline
        }
      );
      return true;
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.error("/goal_tasks/update error", err.response?.data);
        console.error(err.response?.data?.detail ?? "目標タスクの更新に失敗しました");
      } else {
        console.error("Unexpected error", err);
      }
      return false;
    }
  };
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const hasExpired = (deadline: string) => {
    return new Date(deadline) < yesterday;
  }
  const style = {
    transform: CSS.Translate.toString(transform),
    touchAction: "none" as const,
    opacity: isDragging ? 0 : 1,
  };

  const onConfirmDelete = async () => {
    setActiveModal("delete");
    onDeleteTask?.(goal_task_id);
    await deleteTaskById(goal_task_id);
  };

  const onConfirmEdit = async () => {
    const isUpdated = await editTaskById(goal_task_id, editedTaskName, editedEstimatedTime, editedDeadline);
    if (!isUpdated) return;
    setActiveModal("edit");
    onTaskEdit?.(goal_task_id, editedTaskName, editedEstimatedTime, editedDeadline.replace(/\//g, "-"));
  };

  const onOpenOperationModal = () => {
    setActiveModal("operation");
  };

  const onOpenDeleteModal = () => {
    setActiveModal("delete");
  };

  const onEditTask = () => {
    setEditedTaskName(goal_task);
    setEditedEstimatedTime(time.toString());
    setEditedDeadline(formatDateForDisplay(deadline));
    setActiveModal("edit");
  };

  return (
    <>
      <div
        ref={setNodeRef}
        style={style}
        {...listeners}
        {...attributes}
        className={` p-3 m-2 bg-white rounded-lg${hasExpired(deadline) ? " border-red-500 text-red-500" : " border-primary text-primary"} shadow-sm cursor-grab active:cursor-grabbing
        flex  justify-between`}
      >
        <div>
          <p>{formatDateForDisplay(deadline)} {time}分</p>
          <p>{goal_task}</p>
        </div>
        <div>
          <BsThreeDots
            className="w-7 h-6"
            onPointerDown={(e) => {
              e.stopPropagation();
            }}
            onMouseDown={(e) => {
              e.stopPropagation();
            }}
            onTouchStart={(e) => {
              e.stopPropagation();
            }}
            onClick={(e) => {
              e.stopPropagation();
              onOpenOperationModal();
            }}
          />
        </div>
      </div>
      <OperationModal
        operation={["タスクを削除", "タスクを編集"]}
        titles={["タスクを削除", "タスクを編集"]}
        isOpen={activeModal === "operation"}
        onClose={() => setActiveModal(null)}
        handleEdit={onEditTask}
        handleDelete={onOpenDeleteModal}
      />
      <TwoButtonModal
        title="タスク削除"
        content="タスクを削除しますか？"
        hasPartyPopper={false}
        hasTwoButtons={true}
        isOpen={activeModal === "delete"}
        onClose={() => setActiveModal(null)}
        onClickChange={onConfirmDelete}
      />
      <TaskConfigModal
        isOpen={activeModal === "edit"}
        taskName={editedTaskName}
        estimatedTime={editedEstimatedTime}
        deadline={editedDeadline}
        onClose={() => setActiveModal(null)}
        onChangeTaskName={setEditedTaskName}
        onChangeEstimatedTime={setEditedEstimatedTime}
        onChangeDeadline={setEditedDeadline}
        onClickChange={onConfirmEdit}
      />
    </>
  );
};