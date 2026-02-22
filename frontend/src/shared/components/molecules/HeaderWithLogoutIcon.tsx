import { memo } from "react";
import { useNavigate } from "react-router-dom";
import { Logo } from "../atoms/Logo";
import LogoutIcon from "../../../assets/logout.png";
import { useAuth } from "../../../features/users/auth/useAuth";
import type { HeaderWithLogoutIconProps } from "../../types/headerWithLogoutIcon";



export const HeaderWithLogoutIcon = memo(({ onLogoutClick }: HeaderWithLogoutIconProps) => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogoutClick = async () => {
    if (onLogoutClick) {
      await onLogoutClick();
      return;
    }
    const isLoggedOut = await logout();
    if (!isLoggedOut) {
      return;
    }
    navigate("/logout", { replace: true });
  };

  return (
    <div className="bg-primary flex justify-between h-24.5">
      <Logo fontSize="text-2xl" imageSize="w-[35px] h-[35px]" />
      <div className="flex items-center">
        <img src={LogoutIcon} alt="Logout" className="w-8.75 h-8.75" onClick={handleLogoutClick} />
      </div>
    </div>
  )
})