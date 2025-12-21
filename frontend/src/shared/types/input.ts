import { type ReactNode } from "react";
type FormTextColor = "text-primary" | "text-secondary";
type FormBorderColor = "border-primary" | "border-secondary";
type HandleValueChange = (formName: string, newValue: string) => void;
type InputType = "text" | "password";

export interface InputProps {
  borderColor: FormBorderColor
  textColor: FormTextColor
  formName: string
  formType?: InputType
  handleValueChange: HandleValueChange
  children: ReactNode
}