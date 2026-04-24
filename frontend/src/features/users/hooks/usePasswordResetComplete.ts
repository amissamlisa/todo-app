import { useNavigate } from "react-router-dom";

export const usePasswordResetComplete = () => {
  const navigate = useNavigate();

  const handleNavigateToLogin = () => {
    navigate("/", { replace: true });
  };

  return {
    handleNavigateToLogin,
  };
};
