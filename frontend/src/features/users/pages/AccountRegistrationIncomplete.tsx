import { memo, useEffect } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import { Incomplete } from "../../../shared/components/pages/Incomplete";


export const AccountRegistrationIncomplete = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();
  const errMessage = location.state?.error || "アカウント登録に失敗しました";

  useEffect(() => {
    if (!errMessage) {
      navigate("/", { replace: true });
    }
  }, [errMessage, navigate]);

  if (!errMessage) {
    return null;
  }

  const onButtonClick = () => {
    navigate("/", { replace: true });
  }

  return (
    <Incomplete
      title="アカウント登録失敗"
      message={errMessage}
      buttonText="ログイン画面へ"
      hasLogoutButton={false}
      onButtonClick={onButtonClick}
    />
  )
})