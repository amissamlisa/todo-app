import { useNavigate } from "react-router-dom";
import { useAuth } from "../../features/users/auth/useAuth";
import type { UseLogoutButtonParams } from "../types/logoutButton";

export const useLogoutButton = ({ onClick }: UseLogoutButtonParams) => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogoutClick = async () => {
    if (onClick) {
      await onClick();
      return;
    }

    await logout();
    navigate("/", { replace: true });
  };

  return {
    handleLogoutClick,
  };
};