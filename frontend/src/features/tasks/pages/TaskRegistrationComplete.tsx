import { memo } from "react";
import { HeaderWithLogoutIcon } from "../../../shared/components/molecules/HeaderWithLogoutIcon";
import rainbowImg from "../../../assets/rainbow.png";
import { Button } from "../../../shared/components/atoms/Button";
import { useTaskRegistrationComplete } from "../hooks/useTaskRegistrationComplete";

export const TaskRegistrationComplete = memo(() => {
  const { invalidState, handleMoveTop } = useTaskRegistrationComplete();

  if (invalidState) {
    return null;
  }

  return (
    <div className="overflow-y-auto h-screen ">
      <HeaderWithLogoutIcon />
      <div className="flex flex-col justify-center items-center">
        <h2 className="text-primary mt-[clamp(15px,9.1vh,60px)] mb-[clamp(20px,4.7vh,80px)] text-2xl">
          目標タスク登録完了
        </h2>
        <h2 className="text-primary">目標タスク登録が完了しました</h2>
        <img className=" w-[clamp(115px,59.2vw,462px)] " src={rainbowImg} />
        <div className="mb-[clamp(251px,59.5vh,1006px)]">
          <Button onClick={handleMoveTop} buttonColor="bg-primary" textColor="text-secondary">
            TOP画面へ
          </Button>
        </div>
      </div>
    </div>
  );
});
