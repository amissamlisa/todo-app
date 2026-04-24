import { memo } from "react";
import type { InputProps } from "../../types/input";

export const Input = memo(({ textColor, borderColor, children, formType, value, onChangeText, onBlur, name, placeholder, readOnly, disabled }: InputProps) => {
  return (
    <div className="flex flex-col w-[clamp(93px,68vw,400px)]">
      <label className={`${textColor} font-bold`} htmlFor={`${name}`}>{children}</label>
      <input className={`${borderColor} focus:outline-none 
  rounded-[5px] w-full p-2  border-4 border-solid block bg-secondary disabled:bg-gray-200 disabled:text-gray-500 disabled:border-gray-300 disabled:cursor-not-allowed`} type={formType} id={name} name={name} value={value}
        onChange={(e) => onChangeText?.(e.target.value)}
        onBlur={onBlur}
        placeholder={placeholder}
        readOnly={readOnly}
        disabled={disabled}
      />
    </div>
  )
})