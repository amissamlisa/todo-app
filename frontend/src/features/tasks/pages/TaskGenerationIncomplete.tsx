import { memo, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Incomplete } from "../../../shared/components/pages/Incomplete";

export const TaskGenerationIncomplete = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();
  const errMessage = location.state?.error || "目標タスクの生成に失敗しました";

  useEffect(() => {
    if (!errMessage) {
      navigate("/top", { replace: true });
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
      title="目標タスク生成失敗"
      message={errMessage}
      buttonText="TOP画面へ"
      hasLogoutButton={true}
      onButtonClick={onButtonClick}
    />
  );
});
