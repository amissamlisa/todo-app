export type OperationModalProps = {
  operation: string[];
  titles: string[];
  isOpen: boolean;
  onClose: () => void;
  onEdit: () => void;
  onDelete: () => void;
};