import { memo } from "react";
import { Logo } from "../atoms/Logo";
import LogoutIcon from "../../../assets/logout.png";

type HeaderWithLogoutIconProps = {
  onLogoutClick: () => void;
};

export const HeaderWithLogoutIcon = memo(({ onLogoutClick }: HeaderWithLogoutIconProps) => {
  return (
    <div className="bg-primary flex justify-between h-24.5">
      <Logo fontSize="text-2xl" imageSize="w-[35px] h-[35px]" />
      <div className="flex items-center">
        <img src={LogoutIcon} alt="Logout" className="w-8.75 h-8.75" onClick={onLogoutClick} />
      </div>
    </div>
  )
})