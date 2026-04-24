import { useNavigate } from "react-router-dom";

export const usePasswordResetIncomplete = () => {
  const navigate = useNavigate();

  const handleNavigateToLogin = () => {
    navigate("/", { replace: true });
  };

  return {
    handleNavigateToLogin,
  };
};
