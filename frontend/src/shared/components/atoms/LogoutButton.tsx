import LogoutIcon from "../../../assets/logout-btn.png";
import { useLogoutButton } from "../../hooks/useLogoutButton";
import type { LogoutButtonProps } from "../../types/logoutButton";

export const LogoutButton = ({ onClick, className }: LogoutButtonProps) => {
  const { handleLogoutClick } = useLogoutButton({ onClick });

  return (
    <img
      src={LogoutIcon}
      alt="Logout"
      className={className ?? "w-8.75 h-8.75"}
      onClick={handleLogoutClick}
    />
  );
};
