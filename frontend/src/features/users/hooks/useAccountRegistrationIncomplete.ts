import { useNavigate } from "react-router-dom";

export const useAccountRegistrationIncomplete = () => {
  const navigate = useNavigate();

  const handleNavigateToLogin = () => {
    navigate("/", { replace: true });
  };

  return {
    registrationErrorMessage: "アカウント登録に失敗しました",
    handleNavigateToLogin,
  };
};
