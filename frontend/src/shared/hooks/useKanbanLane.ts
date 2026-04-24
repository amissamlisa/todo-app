import { useState } from "react";
import type { UseKanbanLaneParams } from "../types/kanbanLane";

export const useKanbanLane = ({
  canAddTask,
  onAddTask,
}: UseKanbanLaneParams) => {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [newTaskName, setNewTaskName] = useState("");
  const [newEstimatedTime, setNewEstimatedTime] = useState("");
  const [newDeadline, setNewDeadline] = useState("");
  const [addErrorMessage, setAddErrorMessage] = useState("");

  const handleOpenAddModal = () => {
    if (!canAddTask) return;
    setNewTaskName("");
    setNewEstimatedTime("");
    setNewDeadline("");
    setAddErrorMessage("");
    setIsAddModalOpen(true);
  };

  const handleConfirmAdd = async () => {
    const isAdded = await onAddTask?.(newTaskName, newEstimatedTime, newDeadline);
    if (!isAdded) {
      setAddErrorMessage("タスク追加に失敗しました");
      return;
    }

    setAddErrorMessage("");
    setIsAddModalOpen(false);
  };

  const handleChangeTaskName = (value: string) => {
    setNewTaskName(value);
    setAddErrorMessage("");
  };

  const handleChangeEstimatedTime = (value: string) => {
    setNewEstimatedTime(value);
    setAddErrorMessage("");
  };

  const handleChangeDeadline = (value: string) => {
    setNewDeadline(value);
    setAddErrorMessage("");
  };

  return {
    isAddModalOpen,
    setIsAddModalOpen,
    newTaskName,
    newEstimatedTime,
    newDeadline,
    addErrorMessage,
    handleOpenAddModal,
    handleConfirmAdd,
    handleChangeTaskName,
    handleChangeEstimatedTime,
    handleChangeDeadline,
  };
};