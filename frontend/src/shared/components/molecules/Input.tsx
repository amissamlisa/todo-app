import { memo } from "react";
import type { InputProps } from "../../types/input";

export const Input = memo(({ textColor, borderColor, children, formName, formType }: InputProps) => {
  return (
    <div className="flex flex-col w-[clamp(93px,68vw,400px)]">
      <label className={`${textColor} font-bold`}  htmlFor={`${formName}`}>{children}</label>
      <input className={`${borderColor} focus:outline-none 
 rounded-[5px] w-full p-2  border-4 border-solid block bg-secondary`} type={`${formType}`} name={`${formName}`} />
    </div>
  )
})