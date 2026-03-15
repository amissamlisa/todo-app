export interface TwoButtonModalProps {
  title: string;
  content: string;
  showFlag: boolean;
  hasPartyPopper?: boolean;
  hasTwoButtons?: boolean;
  setIsOpenModal: (isOpen: boolean) => void;
  onClickChange?: () => void;
}