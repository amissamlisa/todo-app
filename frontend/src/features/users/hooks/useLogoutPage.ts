import { useNavigate } from "react-router-dom";

export const useLogoutPage = () => {
  const navigate = useNavigate();

  const handleNavigateToLogin = () => {
    navigate("/", { replace: true });
  };

  return {
    handleNavigateToLogin,
  };
};
