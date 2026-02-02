type ButtonBgColor = "bg-primary" | "bg-secondary";
type ButtonTextColor = "text-primary" | "text-secondary";

export interface TwoButtonProps {
  buttonTitle1: string
  buttonTitle2: string
  buttonBgColor: ButtonBgColor
  buttonTextColor: ButtonTextColor
  onPrimaryClick: () => void;
  onSecondaryClick: () => void;
}