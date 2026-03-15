import { useNavigate } from "react-router-dom";
import LogoutIcon from "../../../assets/logout.png";
import { useAuth } from "../../../features/users/auth/useAuth";

type LogoutButtonProps = {
  onLogoutClick?: () => void | Promise<void>;
  className?: string;
};

export const LogoutButton = ({ onLogoutClick, className }: LogoutButtonProps) => {
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
    navigate("/", { replace: true });
  };

  return (
    <img
      src={LogoutIcon}
      alt="Logout"
      className={className ?? "w-8.75 h-8.75"}
      onClick={handleLogoutClick}
    />
  );
};
