import { useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { registerAccount } from "../api/authApi";
import { useAuth } from "../auth/useAuth";
import type { RegistrationFormType } from "../types/registrationForm";

export const useAccountRegistrationConfirm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { api } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const registrationData = (location.state as RegistrationFormType | null) ?? null;
  const userInfoList = useMemo(
    () => registrationData
      ? [
        { title: "ユーザー名", value: registrationData.username },
        { title: "メールアドレス", value: registrationData.email },
        { title: "パスワード", value: registrationData.password },
      ]
      : [],
    [registrationData]
  );

  const handleRegisterAccount = async () => {
    if (!registrationData) {
      navigate("/", { replace: true });
      return;
    }

    try {
      setIsLoading(true);
      await registerAccount(api, registrationData);
      navigate("/user-registration/complete", { replace: true });
    } catch (err) {
      if (!axios.isAxiosError(err)) {
        console.error("Unexpected error", err);
        return;
      }

      if (!err.response) {
        navigate("/server-connection-incomplete", { replace: true });
        return;
      }

      navigate("/user-registration/incomplete", {
        replace: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleNavigateToRegistration = () => {
    navigate("/user-registration", { replace: true });
  };

  return {
    isLoading,
    registrationData,
    userInfoList,
    handleRegisterAccount,
    handleNavigateToRegistration,
  };
};
