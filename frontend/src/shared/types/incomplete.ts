import { type ReactNode } from "react";

export type IncompleteProps = {
  title: string;
  message: ReactNode;
  buttonText?: string;
  hasLogoutButton: boolean;
  onClick?: () => void;
  hasButton?: boolean;
};