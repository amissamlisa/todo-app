import { useLocation, useNavigate } from "react-router-dom";

export const useTaskGenerationIncomplete = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const errorMessage = location.state?.error || "目標タスクの生成に失敗しました";

  const handleNavigateTop = () => {
    navigate("/top", { replace: true });
  };

  return {
    errorMessage,
    handleNavigateTop,
  };
};
