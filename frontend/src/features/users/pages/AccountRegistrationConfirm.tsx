import { memo } from "react";
import { Header } from "../../../shared/components/molecules/Header";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";
import { RegistrationConfirmForm } from "../../../shared/components/molecules/RegistrationConfirmForm";
import { LoadingSpinner } from "../../../shared/components/atoms/LoadingSpinner";
import { useAccountRegistrationConfirm } from "../hooks/useAccountRegistrationConfirm";

export const AccountRegistrationConfirm = memo(() => {
  const {
    isLoading,
    registrationData,
    userInfoList,
    handleRegisterAccount,
    handleNavigateToRegistration,
  } = useAccountRegistrationConfirm();
  if (isLoading) {
    return <LoadingSpinner message="新規会員登録中..." />;
  }
  if (!registrationData) {
    return null;
  }
  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="bg-secondary flex flex-col items-center">
        <h1 className="text-primary mt-[clamp(15px,4vh,60px)] mb-[clamp(20px,4.8vh,80px)] text-2xl">新規会員登録確認</h1>
        <div className="mt-[clamp(15px,4vh,60px) mb-[clamp(10px,2.6vh,40px)]">
          <RegistrationConfirmForm height="h-[clamp(110px,26vh,440px)]" titleColor="text-primary" subTitleColor="text-secondary" backgroundColor="bg-primary" data={userInfoList}>会員情報</RegistrationConfirmForm>
        </div>
        <div className="mt-[clamp(76.5px,18.1vh,306px)] mb-24.5">
          <TwoButton buttonTitle1="登録" buttonTitle2="戻る" buttonBgColor="bg-primary" buttonTextColor="text-secondary" onPrimaryClick={handleRegisterAccount} onSecondaryClick={handleNavigateToRegistration} />
        </div>
      </div>
    </div>
  );
});