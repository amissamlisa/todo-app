export type TwoButtonModalProps = {
  title: string;
  content: string;
  isOpen: boolean;
  hasPartyPopper?: boolean;
  hasTwoButtons?: boolean;
  onClose: () => void;
  onClickChange?: () => void;
};