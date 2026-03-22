import { memo, useEffect, useState } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import { Header } from "../../../shared/components/molecules/Header";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";
import { RegistrationConfirmForm } from "../../../shared/components/molecules/RegistrationConfirmForm";
import type { RegistrationFormType } from "../types/registrationForm";
import { LoadingSpinner } from "../../../shared/components/atoms/LoadingSpinner";
import { useAuth } from "../auth/useAuth";
import axios from "axios";

export const AccountRegistrationConfirm = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();
  const { api } = useAuth();

  const data = location.state as RegistrationFormType;
  const [isLoading, setIsLoading] = useState(false);
  useEffect(() => {
    if (!data) {
      navigate("/", { replace: true });
    }
  }, [data, navigate]);

  if (!data) {
    return null;
  }

  const userData = [
    { title: "ユーザー名", value: data.username },
    { title: "メールアドレス", value: data.email },
    { title: "パスワード", value: data.password }
  ]

  const setAccountInfo = async (body: RegistrationFormType) => {
    const response = await api.post("/auth/registration", body);
    return response.data;
  };

  const onPrimaryClick = async () => {
    try {
      setIsLoading(true);
      await setAccountInfo(data);
      navigate("/user-registration/complete", { replace: true });
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (!err.response) {
          navigate("/server-connection-incomplete", {
            replace: true,
          });
          return;
        }
        navigate("/user-registration/incomplete", {
          state: {
            error: err.response?.data?.detail ?? "アカウント登録に失敗しました",
          },
          replace: true,
        });
      } else {
        console.error("Unexpected error", err);
      }
    } finally {
      setIsLoading(false);
    }
  };
  const onSecondaryClick = () => {
    navigate("/user-registration", { replace: true });
  }
  if (location.key === 'default') {
    return null;
  }
  if (isLoading) {
    return <LoadingSpinner message="新規会員登録中..." />;
  }

  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="bg-secondary flex flex-col items-center">
        <h1 className="text-primary mt-[clamp(15px,4vh,60px)] mb-[clamp(20px,4.8vh,80px)] text-2xl">新規会員登録確認</h1>
        <div className="mt-[clamp(15px,4vh,60px) mb-[clamp(10px,2.6vh,40px)]">
          <RegistrationConfirmForm height="h-[clamp(110px,26vh,440px)]" titleColor="text-primary" subTitleColor="text-secondary" backgroundColor="bg-primary" data={userData}>会員情報</RegistrationConfirmForm>
        </div>
        <div className="mt-[clamp(76.5px,18.1vh,306px)] mb-24.5">
          <TwoButton buttonTitle1="登録" buttonTitle2="戻る" buttonBgColor="bg-primary" buttonTextColor="text-secondary" onPrimaryClick={onPrimaryClick} onSecondaryClick={onSecondaryClick} />
        </div>
      </div>
    </div>
  );
});