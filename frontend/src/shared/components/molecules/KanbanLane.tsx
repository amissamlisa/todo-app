import { useDroppable } from "@dnd-kit/core";
import { useState } from "react";
import { KanbanCard } from "../atoms/KanbanCard";
import { FaPlus } from "react-icons/fa";
import { TaskConfigModal } from "./TaskConfigModal";
import type { KanbanLaneProps } from "../../types/kanbanLane";

export default function KanbanLane({ title, items, bgColor, isAddTaskEnabled = true, onDeleteTasks, onEditTasks, onAddTask }: KanbanLaneProps) {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [newTaskName, setNewTaskName] = useState("");
  const [newEstimatedTime, setNewEstimatedTime] = useState("");
  const [newDeadline, setNewDeadline] = useState("");
  const [addErrorMessage, setAddErrorMessage] = useState("");

  const { setNodeRef } = useDroppable({
    id: `lane-${title}`,
    data: {
      lane: title,
    },
  });

  const onOpenAddModal = () => {
    if (!isAddTaskEnabled) return;
    setNewTaskName("");
    setNewEstimatedTime("");
    setNewDeadline("");
    setAddErrorMessage("");
    setIsAddModalOpen(true);
  };

  const onConfirmAdd = async () => {
    const isAdded = await onAddTask?.(newTaskName, newEstimatedTime, newDeadline);
    if (!isAdded) {
      setAddErrorMessage("タスク追加に失敗しました");
      return;
    }

    setAddErrorMessage("");
    setIsAddModalOpen(false);
  };

  return (
    <div className="flex flex-row mb-[clamp(16px,3.7vh,64px)]">
      <div className="relative flex flex-col items-center mr-2" style={{ height: "clamp(77px,18.2vh,308px)" }}>
        <p className="text-secondary text-xs leading-none">高</p>
        <div className="flex-1 flex flex-col items-center py-0.5">
          <div className="w-0 h-0 border-l-8 border-r-8 border-b-16 border-l-transparent border-r-transparent" style={{ borderBottomColor: bgColor }}></div>
          <div className="flex-1 w-1" style={{ backgroundColor: bgColor }}></div>
          <div className="w-0 h-0 border-l-8 border-r-8 border-t-16 border-l-transparent border-r-transparent" style={{ borderTopColor: bgColor }}></div>
        </div>
        <p className="text-secondary text-xs leading-none">低</p>
      </div>

      <div className="overflow-y-auto h-[clamp(77px,18.2vh,308px)] w-[clamp(143px,73.3vw,572px)] flex flex-col">
        <div
          ref={setNodeRef}
          className="rounded-lg flex-1 p-2 flex flex-col" style={{ backgroundColor: bgColor }}
        >
          <p className="font-bold text-secondary text-center">{title}</p>
          <div className="bg-secondary rounded-lg m-2">
            <div
              className={`text-primary text-center flex items-center justify-center p-3 ${isAddTaskEnabled ? "cursor-pointer" : "cursor-not-allowed bg-gray opacity-50"}`}
              aria-disabled={!isAddTaskEnabled}
            >
              タスクを追加
              <FaPlus className="ml-2" onClick={onOpenAddModal} />
            </div>
          </div>
          {items.map(({ goal_task, time, deadline, goal_task_id }, key) => (
            <KanbanCard goal_task={goal_task} key={goal_task_id} index={key} parent={title} time={time} deadline={deadline} goal_task_id={goal_task_id} onDeleteTask={onDeleteTasks} onTaskEdit={onEditTasks} />
          ))}
        </div>
      </div>
      <TaskConfigModal
        showFlag={isAddModalOpen}
        title="タスクを追加"
        taskName={newTaskName}
        estimatedTime={newEstimatedTime}
        deadline={newDeadline}
        errorMessage={addErrorMessage}
        setIsOpenModal={setIsAddModalOpen}
        onChangeTaskName={(value) => {
          setNewTaskName(value);
          setAddErrorMessage("");
        }}
        onChangeEstimatedTime={(value) => {
          setNewEstimatedTime(value);
          setAddErrorMessage("");
        }}
        onChangeDeadline={(value) => {
          setNewDeadline(value);
          setAddErrorMessage("");
        }}
        onClickChange={onConfirmAdd}
      />
    </div>
  );
}