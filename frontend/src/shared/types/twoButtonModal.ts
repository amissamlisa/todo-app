export interface TwoButtonModalProps {
  title: string;
  content: string;
  showFlag: boolean;
  hasPartyPopper?: boolean;
  setIsOpenModal: (isOpen: boolean) => void;
  onClickChange: () => void;
}