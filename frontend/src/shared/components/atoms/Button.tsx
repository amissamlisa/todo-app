import type { ButtonProps } from "../../types/button";
import { memo } from "react";


export const Button = memo(({ buttonColor, textColor, children, onClick}: ButtonProps) => {
  return (
    <div className="w-[clamp(93px,68vw,400px)]">
      <button onClick={onClick} className={`w-full rounded-full py-3 shadow-xl  ${buttonColor} ${textColor}`} >{children}</button>
    </div>
  )
})