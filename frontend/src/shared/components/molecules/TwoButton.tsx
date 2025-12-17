import { memo } from "react";
import { Button } from "../atoms/Button";
import type { TwoButtonProps } from "../../types/twoButton";

export const TwoButton = memo(({ buttonTitle1, buttonTitle2 }: TwoButtonProps) => {
  return (
    <div >
      <div className="mb-[3vh]">
        <Button buttonColor="bg-secondary" textColor="text-primary">{buttonTitle1}</Button>
      </div>
      <Button buttonColor="bg-secondary" textColor="text-primary">{buttonTitle2}</Button>
    </div>
  )
})