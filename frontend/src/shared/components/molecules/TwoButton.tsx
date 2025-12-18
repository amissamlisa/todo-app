import { memo } from "react";
import { Button } from "../atoms/Button";
import type { TwoButtonProps } from "../../types/twoButton";

export const TwoButton = memo(({ buttonTitle1, buttonTitle2, buttonBgColor, buttonTextColor }: TwoButtonProps) => {
  return (
    <div >
      <div className="mb-[3vh]">
        <Button buttonColor={buttonBgColor} textColor={buttonTextColor}>{buttonTitle1}</Button>
      </div>
      <Button buttonColor={buttonBgColor} textColor={buttonTextColor}>{buttonTitle2}</Button>
    </div>
  )
})