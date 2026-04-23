import { useDroppable } from "@dnd-kit/core";
import { KanbanCard } from "../atoms/KanbanCard";
import { FaPlus } from "react-icons/fa";
import { TaskConfigModal } from "./TaskConfigModal";
import type { KanbanLaneProps } from "../../types/kanbanLane";
import { useKanbanLane } from "../../hooks/useKanbanLane";

export default function KanbanLane({ title, items, bgColor, canAddTask = true, onDeleteTasks, onEditTasks, onAddTask }: KanbanLaneProps) {
  const {
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
  } = useKanbanLane({
    canAddTask,
    onAddTask,
  });

  const { setNodeRef } = useDroppable({
    id: `lane-${title}`,
    data: {
      lane: title,
    },
  });

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
            <button
              onClick={canAddTask ? handleOpenAddModal : undefined}
              disabled={!canAddTask}
              className={`w-full text-primary flex items-center justify-center gap-2 p-3 ${canAddTask
                  ? "cursor-pointer"
                  : "cursor-not-allowed bg-gray opacity-50"
                }`}
            >
              <span>タスクを追加</span>
              <FaPlus />
            </button>
          </div>
          {items.map(({ goalTask, time, deadline, goalTaskId }, key) => (
            <KanbanCard goalTask={goalTask} key={goalTaskId} index={key} parent={title} time={time} deadline={deadline} goalTaskId={goalTaskId} onDeleteTask={onDeleteTasks} onTaskEdit={onEditTasks} />
          ))}
        </div>
      </div>
      <TaskConfigModal
        isOpen={isAddModalOpen}
        title="タスクを追加"
        taskName={newTaskName}
        estimatedTime={newEstimatedTime}
        deadline={newDeadline}
        errorMessage={addErrorMessage}
        onClose={() => setIsAddModalOpen(false)}
        onChangeTaskName={handleChangeTaskName}
        onChangeEstimatedTime={handleChangeEstimatedTime}
        onChangeDeadline={handleChangeDeadline}
        onClickChange={handleConfirmAdd}
      />
    </div>
  );
}