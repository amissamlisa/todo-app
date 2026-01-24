import { memo } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import axios from "axios";
import { Header } from "../../../shared/components/molecules/Header";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";
import { RegistrationConfirmForm } from "../../../shared/components/molecules/RegistrationConfirmForm";
import type { RegistrationFormType } from "../types/registrationForm";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const url = API_BASE_URL + "/auth/registration";

export const AccountRegistrationConfirm = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();

  const data = location.state as RegistrationFormType;

  const userData = [
    { title: "ユーザー名", value: data.username },
    { title: "メールアドレス", value: data.email },
    { title: "パスワード", value: data.password }
  ]

  const setAccountInfo = async (body: RegistrationFormType) => {
    const response = await axios.post(url, body);
    return response.data;
  };

  const onPrimaryClick = async () => {
    try {
      await setAccountInfo(data);
      navigate("/user-registration/complete", { replace: true });
    } catch (err) {
      if (axios.isAxiosError(err)) {
        navigate("/user-registration/incomplete", {
          state: {
            error: err.response?.data?.detail ?? "アカウント登録に失敗しました",
          },
          replace: true,
        });
      } else {
        console.error("予期しないエラー", err);
      }
    }
  };
  const onSecondaryClick = () => {
    navigate("/user-registration", { replace: true });
  }
  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="bg-secondary flex flex-col items-center">
        <h1 className="text-primary mt-[clamp(15px,4vh,60px)] mb-[clamp(20px,4.8vh,80px)] text-2xl">新規会員登録確認</h1>
        <div className="mt-[clamp(15px,4vh,60px) mb-[clamp(10px,2.6vh,40px)]">
          <RegistrationConfirmForm titleColor="text-primary" subTitleColor="text-secondary" backgroundColor="bg-primary" data={userData}>会員情報</RegistrationConfirmForm>
        </div>
        <div className="mt-[clamp(76.5px,18.1vh,306px)] mb-24.5">
          <TwoButton buttonTitle1="登録" buttonTitle2="戻る" buttonBgColor="bg-primary" buttonTextColor="text-secondary" onPrimaryClick={onPrimaryClick} onSecondaryClick={onSecondaryClick} />
        </div>
      </div>
    </div>
  );
});