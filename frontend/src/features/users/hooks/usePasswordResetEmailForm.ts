import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../auth/useAuth";
import type { PasswordResetEmailType } from "../types/passwordResetEmail";

export const usePasswordResetEmailForm = () => {
  const navigate = useNavigate();
  const { sendPasswordResetEmail } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const handlePasswordResetEmail = async (data: PasswordResetEmailType) => {
    setIsLoading(true);
    try {
      await sendPasswordResetEmail(data.email);
      navigate("/password-reset-message-sent", { replace: true });
    } catch (err: unknown) {
      if (!axios.isAxiosError(err)) {
        console.error("Unexpected error", err);
        return;
      }
      if (!err.response) {
        navigate("/server-connection-incomplete", { replace: true });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleNavigateToLogin = () => {
    navigate("/", { replace: true });
  };

  return {
    isLoading,
    handlePasswordResetEmail,
    handleNavigateToLogin,
  };
};
