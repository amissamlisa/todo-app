import { memo } from "react";
import { type RegistrationConfirmFormProps } from "../../types/registrationConfirmForm";

export const RegistrationConfirmForm = memo(({ children, data, titleColor, subTitleColor, backgroundColor, height, width, centerItems }: RegistrationConfirmFormProps) => {
  const heightClass = height ?? "h-screen";
  const widthClass = width ?? "w-[clamp(93px,68vw,400px)]";
  const itemClassName = `mt-[clamp(15px,3.5vh,60px)] mb-[clamp(15px,3.5vh,60px)]${centerItems ? " text-center" : " ml-[clamp(5px,2.5vh,20px)]"
    }`;
  return (
    <div className={`flex flex-col ${widthClass}`}>
      <p className={`${titleColor} font-bold text-center mb-[clamp(7px,1.6vh,28px)]`}>{children}</p>
      <div className={`${subTitleColor} ${backgroundColor} rounded-[5px] overflow-y-auto p-[4.3vw] ${heightClass}`}>
        {data.map((data) => (
          <div key={data.title} className={itemClassName}>
            {data.title ? <p>{data.title}</p> : null}
            {data.title === "パスワード" ? <p>●●●●●●</p> : <p>{data.value}</p>}
          </div>
        ))}
      </div>
    </div>
  )
})