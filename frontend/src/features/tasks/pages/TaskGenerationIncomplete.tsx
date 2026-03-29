import { memo } from "react";
import { Incomplete } from "../../../shared/components/pages/Incomplete";
import { useTaskGenerationIncomplete } from "../hooks/useTaskGenerationIncomplete";

export const TaskGenerationIncomplete = memo(() => {
  const { errorMessage, handleNavigateTop } = useTaskGenerationIncomplete();

  return (
    <Incomplete
      title="目標タスク生成失敗"
      message={errorMessage}
      buttonText="TOP画面へ"
      hasLogoutButton={true}
      onClick={handleNavigateTop}
    />
  );
});
