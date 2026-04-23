import type { ButtonProps } from "../../types/button";
import { memo } from "react";


export const ModalButton = memo(({ buttonColor, textColor, children, onClick}: ButtonProps) => {
  return (
    <div className="h-[clamp(12.5px,2.9vh,50px) w-[clamp(36px,18.4vw,144px)]">
      <button onClick={onClick} className={`w-full h-full rounded-xs shadow-xl  ${buttonColor} ${textColor}`} >{children}</button>
    </div>
  )
})