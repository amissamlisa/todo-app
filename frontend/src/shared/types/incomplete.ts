import { type ReactNode } from "react";

export interface IncompleteProps {
  title: string;
  message: ReactNode;
  buttonText?: string;
  hasLogoutButton: boolean;
  onButtonClick?: () => void;
  hasButton?: boolean;
};