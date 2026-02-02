import { type ReactNode } from "react";

export interface RegistrationConfirmFormProps {
  children: ReactNode;
  titleColor: string;
  subTitleColor: string;
  backgroundColor: string;
  data: {
    title: string;
    value: string;
  }[]
}