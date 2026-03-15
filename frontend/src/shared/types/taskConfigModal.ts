export interface TaskConfigModalProps {
  showFlag: boolean;
  taskName: string;
  estimatedTime: string;
  deadline: string;
  errorMessage?: string;
  title?: string;
  hasTwoButtons?: boolean;
  setIsOpenModal: (isOpen: boolean) => void;
  onChangeTaskName: (value: string) => void;
  onChangeEstimatedTime: (value: string) => void;
  onChangeDeadline: (value: string) => void;
  onClickChange?: () => void;
}