import { memo } from "react";
import { Button } from "../atoms/Button";
import type { TwoButtonProps } from "../../types/twoButton";

export const TwoButton = memo(({ buttonTitle1, buttonTitle2, buttonBgColor, buttonTextColor,  onPrimaryClick, onSecondaryClick}: TwoButtonProps) => {
  return (
    <div >
      <div className="mb-[3vh]">
        <Button onButtonClick={onPrimaryClick}  buttonColor={buttonBgColor} textColor={buttonTextColor}  >{buttonTitle1}</Button>
      </div>
      <Button onButtonClick={onSecondaryClick}  buttonColor={buttonBgColor} textColor={buttonTextColor} >{buttonTitle2}</Button>
    </div>
  )
})