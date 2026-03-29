export type TaskConfigModalProps = {
  isOpen: boolean;
  taskName: string;
  estimatedTime: string;
  deadline: string;
  errorMessage?: string;
  title?: string;
  hasTwoButtons?: boolean;
  onClose: () => void;
  onChangeTaskName: (value: string) => void;
  onChangeEstimatedTime: (value: string) => void;
  onChangeDeadline: (value: string) => void;
  onClickChange?: () => void;
};