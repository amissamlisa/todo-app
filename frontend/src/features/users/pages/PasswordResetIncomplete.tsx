import { memo, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Incomplete } from "../../../shared/components/pages/Incomplete";

export const PasswordResetIncomplete = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.key === 'default') {
      navigate("/", { replace: true });
    }
  }, [location.key, navigate]);

  if (location.key === 'default') {
    return null;
  }

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