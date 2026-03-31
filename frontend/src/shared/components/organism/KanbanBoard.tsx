import { DndContext, DragOverlay, rectIntersection } from "@dnd-kit/core";
import KanbanLane from "../molecules/KanbanLane";
import type { KanbanBoardProps } from "../../types/kanbanBoard";
import { useKanbanBoard } from "../../hooks/useKanbanBoard";

export default function KanbanBoard({ TodoItems, canAddTask = true, onPointsChange, onDoneTasksChange, onTodayTasksChange, onDeleteTasks }: KanbanBoardProps) {
  const {
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
  } = useKanbanBoard({
    TodoItems,
    onPointsChange,
    onDoneTasksChange,
    onTodayTasksChange,
    onDeleteTasks,
  });


  return (
    <DndContext
      collisionDetection={rectIntersection}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      onDragCancel={handleDragCancel}
    >
      <div className="flex flex-col">
        <div className="flex flex-col">
          <KanbanLane title="未着手" items={todoItems} bgColor="#FF8E8E" canAddTask={canAddTask} onDeleteTasks={handleDeleteTask} onEditTasks={handleEditTask} onAddTask={(goalTaskName, estimatedTime, deadline) => handleAddTask("未着手", goalTaskName, estimatedTime, deadline)} />
          <KanbanLane title="作業中" items={inProgressItems} bgColor="#FFC68E" canAddTask={canAddTask} onDeleteTasks={handleDeleteTask} onEditTasks={handleEditTask} onAddTask={(goalTaskName, estimatedTime, deadline) => handleAddTask("作業中", goalTaskName, estimatedTime, deadline)} />
          <KanbanLane title="完了" items={doneItems} bgColor="#8EFF8E" canAddTask={canAddTask} onDeleteTasks={handleDeleteTask} onEditTasks={handleEditTask} onAddTask={(goalTaskName, estimatedTime, deadline) => handleAddTask("完了", goalTaskName, estimatedTime, deadline)} />
        </div>
      </div>
      <DragOverlay>
        {activeCard ? (
          <div className="p-3 m-2 bg-white rounded-lg border border-primary text-primary shadow-sm flex justify-between opacity-95 w-[clamp(120px,65vw,540px)]">
            <div>
              <p>{formatDateForDisplay(activeCard.deadline)} {activeCard.time}分</p>
              <p>{activeCard.goalTask}</p>
            </div>
          </div>
        ) : null}
      </DragOverlay>
    </DndContext>
  );
}
