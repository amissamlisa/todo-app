import { useNavigate } from "react-router-dom";

export const usePasswordResetRequestSubmitted = () => {
  const navigate = useNavigate();

  const handleNavigateToLogin = () => {
    navigate("/", { replace: true });
  };

  return {
    handleNavigateToLogin,
  };
};
