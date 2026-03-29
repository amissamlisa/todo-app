import { memo } from "react";
import { ImCross } from "react-icons/im";
import type { OperationModalProps } from "../../types/operationModal";

export const OperationModal = memo(({ operation, titles, isOpen, onClose, handleEdit, handleDelete }: OperationModalProps) => {
  const menuItems = operation.length > 0 ? operation : titles;
  const onSelectOperation = (item: string) => {
    if (item.includes("削除")) {
      handleDelete();
      return;
    }
    if (item.includes("編集")) {
      handleEdit();
    }
  };

  return (
    <>
      {isOpen ? (
        <div
          className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center"
          onClick={onClose}
        >
          <div
            className="w-[clamp(156.5px,80vw,626px)] bg-white rounded-[3px] overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="bg-secondary relative flex items-center justify-center py-3">
              <p className="text-lg text-primary">操作を選択</p>
              <ImCross
                className="absolute right-4 cursor-pointer text-primary"
                onClick={onClose}
              />
            </div>
            <div className="px-3 py-2 flex flex-col gap-2">
              {menuItems.map((item, index) => (
                <button
                  key={index}
                  type="button"
                  className="w-full text-primary bg-secondary rounded-md py-2"
                  onClick={() => onSelectOperation(item)}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <></>
      )}
    </>
  );
});