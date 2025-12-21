import {type ReactNode } from "react"

type ButtonBgColor = "bg-primary" | "bg-secondary";
type ButtonTextColor = "text-primary" | "text-secondary";

export interface ButtonProps {
  buttonColor: ButtonBgColor,
  textColor: ButtonTextColor,
  children: ReactNode,
  onButtonClick: () => void;
}