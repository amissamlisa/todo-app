import type { ButtonProps } from "../../types/button";
import { memo } from "react";


export const Button = memo(({ buttonColor, textColor, children }: ButtonProps) => {
  return (
    <button className={`rounded-full shadow-xl px-[clamp(24px,24vw,100px)] ${buttonColor} ${textColor}`} >{children}</button>
  )
})