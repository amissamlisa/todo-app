export type OperationModalProps = {
  operation: string[];
  titles: string[];
  isOpen: boolean;
  onClose: () => void;
  handleEdit: () => void;
  handleDelete: () => void;
};