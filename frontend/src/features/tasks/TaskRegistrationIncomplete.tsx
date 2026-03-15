import { memo, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Incomplete } from "../../shared/components/pages/Incomplete";

export const TaskRegistrationIncomplete = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();
  const errMessage = location.state?.error || "目標達成タスクの登録に失敗しました";

  useEffect(() => {
    if (!errMessage) {
      navigate("/tasks-registration", { replace: true });
    }
  }, [errMessage, navigate]);

  if (!errMessage) {
    return null;
  }

  const onButtonClick = () => {
    navigate("/top", { replace: true });
  };

  return (
    <Incomplete
      title="タスク登録失敗"
      message={errMessage}
      buttonText="タスク登録画面へ"
      hasLogoutButton={true}
      onButtonClick={onButtonClick}
    />
  );
});
