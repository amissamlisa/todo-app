import {type ReactNode } from "react"

type ButtonBgColor = "bg-primary" | "bg-secondary";
type ButtonTextColor = "text-primary" | "text-secondary";

export type ButtonProps = {
  buttonColor: ButtonBgColor,
  textColor: ButtonTextColor,
  children: ReactNode,
  onClick?: () => void;
};