import { memo } from "react";
import { useState } from "react";
import { IoIosEye } from "react-icons/io";
import { IoIosEyeOff } from "react-icons/io";
import type { InputProps } from "../../types/input";

export const PasswordInput = memo(({ 
  textColor,
  borderColor,
  children, 
  value, 
  onChangeText, onBlur, name }: InputProps) => {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [formType, setFormType] = useState("password");
  const handleEyeClick = (eye: boolean) => {
    setIsPasswordVisible(!eye);
    setFormType(eye ? "password" : "text");
  };
  return (
    <div className="flex relative flex-col w-[clamp(93px,68vw,400px)]">
      <label className={`${textColor} font-bold`} htmlFor={`${name}`}>{children}</label>
      <input value={value}
        onChange={(e) => onChangeText?.(e.target.value)}
        onBlur={onBlur} className={`${borderColor} focus:outline-none 
        rounded-[5px] w-full p-2  border-4 border-solid block bg-secondary`} type={`${formType}`} name={`${name}`} />
        {isPasswordVisible === true && <IoIosEye onClick={() => handleEyeClick(isPasswordVisible)} className="text-primary absolute right-3 bottom-2/12" size={24} />}
        {isPasswordVisible === false && <IoIosEyeOff onClick={() => handleEyeClick(isPasswordVisible)} className="text-primary absolute right-3 bottom-2/12" size={24} />}
    </div>
  )
})