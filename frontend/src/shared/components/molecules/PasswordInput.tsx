import { memo } from "react";
import { useState } from "react";
import { IoIosEye } from "react-icons/io";
import { IoIosEyeOff } from "react-icons/io";
import type { InputProps } from "../../types/input";

export const PasswordInput = memo(({ textColor, borderColor, children, formName}: InputProps) => {
  const [eye, setEye] = useState(false);
  const [formType, setFormType] = useState("password");
  const handleEyeClick = (eye: boolean) => {
    setEye(!eye);
    setFormType(eye ? "password" : "text");
  };
  return (
    <div className="flex relative flex-col w-[clamp(93px,68vw,400px)]">
      <label className={`${textColor} font-bold`} htmlFor={`${formName}`}>{children}</label>
      <input className={`${borderColor} focus:outline-none 
 rounded-[5px] w-full p-2  border-4 border-solid block bg-secondary`} type={`${formType}`} name={`${formName}`} />
      {eye === true && <IoIosEye onClick={() => handleEyeClick(eye)} className="text-primary absolute right-3 bottom-2/12" size={24} />}
      {eye === false && <IoIosEyeOff onClick={() => handleEyeClick(eye)}   className="text-primary absolute right-3 bottom-2/12" size={24}/>}
    </div>
  )
})