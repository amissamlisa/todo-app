export interface OperationModalProps {
  operation: string[];
  titles: string[];
  showFlag: boolean;
  setIsOpenModal: (isOpen: boolean) => void;
  handleEdit: () => void;
  handleDelete: () => void;
}