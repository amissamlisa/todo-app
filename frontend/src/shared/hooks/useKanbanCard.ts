import { useState } from "react";
import axios from "axios";
import { useAuth } from "../../features/users/auth/useAuth";
import { deleteGoalTask, updateGoalTask } from "../api/kanbanApi";
import type { KanbanCardProps } from "../types/kanbanCard";

export const useKanbanCard = ({
  goalTaskId,
  goalTask,
  time,
  deadline,
  onDeleteTask,
  onTaskEdit,
}: KanbanCardProps) => {
  const { api } = useAuth();
  const [activeModal, setActiveModal] = useState<
    "operation" | "delete" | "edit" | null
  >(null);
  const [draftTaskName, setDraftTaskName] = useState(goalTask);
  const [draftEstimatedTime, setDraftEstimatedTime] = useState(time.toString());
  const [draftDeadline, setDraftDeadline] = useState(deadline.replace(/-/g, "/"));

  const formatDateForDisplay = (value: string) => value.replace(/-/g, "/");

  const hasExpired = (value: string) => {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    return new Date(value) < yesterday;
  };

  const confirmDeleteTask = async () => {
    try {
      await deleteGoalTask(api, goalTaskId);
      setActiveModal(null);
      onDeleteTask?.(goalTaskId);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.error("/goal-tasks/{goalTaskId} delete error", err.response?.data);
        console.error(err.response?.data?.detail ?? "目標タスクの登録に失敗しました");
      } else {
        console.error("Unexpected error", err);
      }
    }
  };

  const confirmEditTask = async () => {
    try {
      const normalizedDeadline = draftDeadline.replace(/\//g, "-");
      await updateGoalTask(api, goalTaskId, {
        goalTask: draftTaskName,
        estimatedTime: Number(draftEstimatedTime),
        deadline: normalizedDeadline,
      });
      setActiveModal(null);
      onTaskEdit?.(goalTaskId, draftTaskName, draftEstimatedTime, normalizedDeadline);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.error("/goal-tasks/{goalTaskId} update error", err.response?.data);
        console.error(err.response?.data?.detail ?? "目標タスクの更新に失敗しました");
      } else {
        console.error("Unexpected error", err);
      }
    }
  };

  const openMenuModal = () => {
    setActiveModal("operation");
  };

  const openDeleteModal = () => {
    setActiveModal("delete");
  };

  const openEditModal = () => {
    setDraftTaskName(goalTask);
    setDraftEstimatedTime(time.toString());
    setDraftDeadline(formatDateForDisplay(deadline));
    setActiveModal("edit");
  };

  return {
    activeModal,
    setActiveModal,
    draftTaskName,
    setDraftTaskName,
    draftEstimatedTime,
    setDraftEstimatedTime,
    draftDeadline,
    setDraftDeadline,
    formatDateForDisplay,
    hasExpired,
    confirmDeleteTask,
    confirmEditTask,
    openMenuModal,
    openDeleteModal,
    openEditModal,
  };
};