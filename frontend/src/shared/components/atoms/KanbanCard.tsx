import { useDraggable, useDroppable } from "@dnd-kit/core";
import { CSS } from "@dnd-kit/utilities";
import { TwoButtonModal } from "../molecules/TwoButtonModal";
import { BsThreeDots } from "react-icons/bs";
import { OperationModal } from "../molecules/OperationModal";
import { TaskConfigModal } from "../molecules/TaskConfigModal";
import type { KanbanCardProps } from "../../types/kanbanCard";
import { useKanbanCard } from "../../hooks/useKanbanCard";

export const KanbanCard = ({
  goalTaskId,
  goalTask,
  time,
  deadline,
  index,
  parent,
  onDeleteTask,
  onTaskEdit,
}: KanbanCardProps) => {
  const {
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
  } = useKanbanCard({
    goalTaskId,
    goalTask,
    time,
    deadline,
    index,
    parent,
    onDeleteTask,
    onTaskEdit,
  });
  const {
    attributes,
    listeners,
    setNodeRef: setDraggableRef,
    transform,
    isDragging,
  } = useDraggable({
    id: `goal_task_${goalTaskId}`,
    data: {
      goalTaskId,
      goalTask,
      time,
      index,
      parent,
      deadline,
    },
  });

  const { setNodeRef: setDroppableRef } = useDroppable({
    id: `goal_task_${goalTaskId}`,
    data: {
      lane: parent,
      index,
    },
  });

  const setNodeRef = (node: HTMLDivElement | null) => {
    setDraggableRef(node);
    setDroppableRef(node);
  };
  const style = {
    transform: CSS.Translate.toString(transform),
    touchAction: "none" as const,
    opacity: isDragging ? 0 : 1,
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
          <p>{goalTask}</p>
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
              openMenuModal();
            }}
          />
        </div>
      </div>
      <OperationModal
        operation={["タスクを削除", "タスクを編集"]}
        titles={["タスクを削除", "タスクを編集"]}
        isOpen={activeModal === "operation"}
        onClose={() => setActiveModal(null)}
        onEdit={openEditModal}
        onDelete={openDeleteModal}
      />
      <TwoButtonModal
        title="タスク削除"
        content="タスクを削除しますか？"
        hasPartyPopper={false}
        hasTwoButtons={true}
        isOpen={activeModal === "delete"}
        onClose={() => setActiveModal(null)}
        onClickChange={confirmDeleteTask}
      />
      <TaskConfigModal
        isOpen={activeModal === "edit"}
        taskName={draftTaskName}
        estimatedTime={draftEstimatedTime}
        deadline={draftDeadline}
        onClose={() => setActiveModal(null)}
        onChangeTaskName={setDraftTaskName}
        onChangeEstimatedTime={setDraftEstimatedTime}
        onChangeDeadline={setDraftDeadline}
        onClickChange={confirmEditTask}
      />
    </>
  );
};