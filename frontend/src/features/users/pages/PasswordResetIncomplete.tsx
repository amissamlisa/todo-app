import { memo } from "react";
import { Incomplete } from "../../../shared/components/pages/Incomplete";
import { usePasswordResetIncomplete } from "../hooks/usePasswordResetIncomplete";

export const PasswordResetIncomplete = memo(() => {
  const { handleNavigateToLogin } = usePasswordResetIncomplete();
  return (
    <Incomplete
      title="パスワード再設定失敗"
      message={
        <>
          申し訳ございません。パスワード再設定リンクが無効です。<br />
          再度、リンクを発行しなおしてください
        </>
      }
      buttonText="ログイン画面へ"
      hasLogoutButton={false}
      onClick={handleNavigateToLogin}
    />
  )
})