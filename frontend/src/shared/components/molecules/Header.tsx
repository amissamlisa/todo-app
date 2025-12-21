import { memo } from "react";
import { Logo } from "../atoms/Logo";

export const Header = memo(() => {
  return (
    <div className="bg-primary flex justify-start h-24.5">
      <Logo fontSize="text-2xl" imageSize="w-[35px] h-[35px]" />
    </div>
  )
})