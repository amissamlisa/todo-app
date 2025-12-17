import { type ReactNode } from "react";
type FormTextColor = "text-primary" | "text-secondary";
type FormBorderColor = "border-primary" | "border-secondary";
export interface InputProps {
  borderColor: FormBorderColor
  textColor: FormTextColor
  formName: string,
  formType?: string,
  children: ReactNode
}