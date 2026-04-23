import { memo } from "react";
import { Incomplete } from "../../../shared/components/pages/Incomplete";
import { useTaskRegistrationIncomplete } from "../hooks/useTaskRegistrationIncomplete";

export const TaskRegistrationIncomplete = memo(() => {
  const { errorMessage, handleNavigateTop } = useTaskRegistrationIncomplete();

  return (
    <Incomplete
      title="タスク登録失敗"
      message={errorMessage}
      buttonText="TOP画面へ"
      hasLogoutButton={true}
      onClick={handleNavigateTop}
    />
  );
});
