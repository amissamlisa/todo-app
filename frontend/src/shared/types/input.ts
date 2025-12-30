import { type ReactNode } from "react";
type FormTextColor = "text-primary" | "text-secondary";
type FormBorderColor = "border-primary" | "border-secondary";
type InputType = "text" | "password";

export interface InputProps {
  value?: string;
  onChangeText?: (value: string) => void;
  onBlur?: () => void;
  borderColor: FormBorderColor;
  textColor: FormTextColor;
  name: string;
  formType?: InputType;
  children: ReactNode;
}