import { memo } from "react";
import { type RegistrationConfirmFormProps } from "../../types/registrationConfirmForm";


export const RegistrationConfirmForm = memo(({ children, data, titleColor, subTitleColor, backgroundColor }: RegistrationConfirmFormProps) => {
  return (
    <div className="flex flex-col w-[clamp(93px,68vw,400px)]">
      <p className={`${titleColor} font-bold text-center mb-[clamp(7px,1.6vh,28px)]`}>{children}</p>
      <div className={`${subTitleColor} ${backgroundColor} rounded-[5px]`}>
        {data.map((data) => (
          <div key={data.title} className="mt-[clamp(15px,3.5vh,60px)] ml-[clamp(5px,2.5vh,20px)] mb-[clamp(15px,3.5vh,60px)]">
            <p >{data.title}</p>
            {data.title === "パスワード" ? <p>●●●●●●</p> : <p>{data.value}</p>}
          </div>
        ))} 
      </div>
    </div>
  )
})