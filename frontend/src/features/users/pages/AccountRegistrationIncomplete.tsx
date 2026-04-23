import { memo } from "react";
import { Incomplete } from "../../../shared/components/pages/Incomplete";
import { useAccountRegistrationIncomplete } from "../hooks/useAccountRegistrationIncomplete";

export const AccountRegistrationIncomplete = memo(() => {
  const { registrationErrorMessage, handleNavigateToLogin } = useAccountRegistrationIncomplete();

  return (
    <Incomplete
      title="アカウント登録失敗"
      message={registrationErrorMessage}
      buttonText="ログイン画面へ"
      hasLogoutButton={false}
      onClick={handleNavigateToLogin}
    />
  )
})