import { memo } from "react";
import { useNavigate } from "react-router-dom";
import { Incomplete } from "../../../shared/components/pages/Incomplete";

export const PasswordResetIncomplete = memo(() => {
  const navigate = useNavigate();

  const onButtonClick = () => {
    navigate("/", { replace: true });
  }
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
      onButtonClick={onButtonClick}
    />
  )
})