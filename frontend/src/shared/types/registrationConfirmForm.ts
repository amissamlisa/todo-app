import { type ReactNode } from "react";

export interface RegistrationConfirmFormProps {
  children: ReactNode;
  titleColor: string;
  subTitleColor: string;
  backgroundColor: string;
  height?: string;
  width?: string;
  centerItems?: boolean;
  data: {
    title?: string;
    value: string;
  }[]
}