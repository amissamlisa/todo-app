import { memo } from "react";
import { Logo } from "../atoms/Logo";
import { LogoutButton } from "../atoms/LogoutButton";

export const HeaderWithLogoutIcon = memo(() => {
  return (
    <div className="bg-primary flex justify-between h-24.5">
      <Logo fontSize="text-2xl" imageSize="w-[35px] h-[35px]" />
      <div className="flex items-center">
        <LogoutButton />
      </div>
    </div>
  )
})