import { type ReactNode } from "react";

export type RegistrationConfirmFormProps = {
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
};