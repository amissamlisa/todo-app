import { useNavigate } from "react-router-dom";

export const useAccountRegistrationComplete = () => {
  const navigate = useNavigate();

  const handleNavigateToLogin = () => {
    navigate("/", { replace: true });
  };

  return {
    handleNavigateToLogin,
  };
};
