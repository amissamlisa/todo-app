import { useLocation, useNavigate } from "react-router-dom";

export const useTaskRegistrationIncomplete = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const errorMessage = location.state?.error || "目標達成タスクの登録に失敗しました";

  const handleNavigateTop = () => {
    navigate("/top", { replace: true });
  };

  return {
    errorMessage,
    handleNavigateTop,
  };
};
