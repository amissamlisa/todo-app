import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth";
import type { LoginFormType } from "../types/loginForm";

export const useLoginPage = () => {
  const navigate = useNavigate();
  const { login, loginErrorMessageFromServer, clearLoginErrorMessage } = useAuth();

  const handleLogin = async (data: LoginFormType) => {
    await login(data.email, data.password);
  };

  const handleNavigateToRegistration = () => {
    navigate("/user-registration", { replace: true });
    if (loginErrorMessageFromServer !== null) {
      clearLoginErrorMessage();
    }
  };

  const handleNavigateToPasswordResetEmail = () => {
    if (loginErrorMessageFromServer !== null) {
      clearLoginErrorMessage();
    }
  };

  return {
    loginErrorMessageFromServer,
    handleLogin,
    handleNavigateToRegistration,
    handleNavigateToPasswordResetEmail,
  };
};
