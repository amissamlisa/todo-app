import { memo } from "react";
import { RegistrationConfirmForm } from "../../../shared/components/molecules/RegistrationConfirmForm";
import { HeaderWithLogoutIcon } from "../../../shared/components/molecules/HeaderWithLogoutIcon";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";
import { useTaskUpdateConfirm } from "../hooks/useTaskUpdateConfirm";

export const TaskUpdateConfirm = memo(() => {
  const {
    invalidState,
    goalName,
    items,
    handleUpdateGoalTasks,
    handleNavigateToTop,
  } = useTaskUpdateConfirm();

  if (invalidState) {
    return null;
  }

  return (
    <div className="overflow-y-auto h-screen">
      <HeaderWithLogoutIcon />
      <div className="bg-secondary flex flex-col items-center ">
        <p className="text-primary font-bold text-center mt-[clamp(14px,3.3vh,56px)] mb-[clamp(7px,1.6vh,28px)]">
          達成目標
        </p>
        <div className="text-secondary bg-primary rounded-[5px] overflow-y-auto pl-[4vw] pr-[4vw] h-[clamp(25px,5.9vh,100px)] w-[clamp(163.5px,84vw,654px)] mb-[clamp(10.5px,2.4vh,42px)] flex items-center justify-center text-center">
          <p>{goalName}</p>
        </div>
        <RegistrationConfirmForm
          titleColor="text-primary"
          subTitleColor="text-secondary"
          backgroundColor="bg-primary"
          centerItems={true}
          data={items}
          height="h-[clamp(196px,46vh,784px)]"
          width="w-[clamp(163.5px,84vw,654px)]"
        >
          目標達成タスク一覧
        </RegistrationConfirmForm>
        <div className="mt-[clamp(20px,4.7vh,80px)] mb-24.5">
          <TwoButton
            buttonTitle1="更新"
            buttonTitle2="戻る"
            buttonBgColor="bg-primary"
            buttonTextColor="text-secondary"
            onPrimaryClick={handleUpdateGoalTasks}
            onSecondaryClick={handleNavigateToTop}
          />
        </div>
      </div>
    </div>
  );
});
