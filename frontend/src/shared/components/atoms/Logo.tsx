import logoIcon from "../../../assets/cloud-icon.png"
import { memo } from "react";
import type { LogoProps } from "../../types/logo";

export const Logo = memo(({ fontSize, imageSize }: LogoProps) => {
  return (
    <div className="flex flex-row items-center justify-center">
      <div className="">
        <img src={logoIcon} className={imageSize} alt="logo" />
      </div>
      <h2 className={`font-logo font-bold text-secondary ${fontSize}`}>Claidy TODO</h2>
    </div>
  )
})