import { memo, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { HeaderWithLogoutIcon } from "../../../shared/components/molecules/HeaderWithLogoutIcon";
import rainbowImg from "../../../assets/rainbow.png";
import { Button } from "../../../shared/components/atoms/Button";

export const TaskRegistrationComplete = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state as {
    goal: {
      goal_name: string;
      status_against_goal: string;
      start_day: string;
      target_day: string;
      weekday_available_time: number;
      weekends_available_time: number;
      task_creation_rule?: string;
    };
    goal_tasks: {
      goal_task_name: string;
      deadline: string;
      estimated_time: number;
    }[];
    goal_total_estimated_time?: number;
  } | null;

  useEffect(() => {
    if (location.key === "default" || !state?.goal || !state?.goal_tasks) {
      navigate("/tasks-registration", { replace: true });
    }
  }, [location.key, navigate, state?.goal, state?.goal_tasks]);

  if (location.key === "default" || !state?.goal || !state?.goal_tasks) {
    return null;
  }

  const onButtonClick = () => {
    navigate("/top", {
      replace: true,
      state: {
        goal: state.goal,
        goal_tasks: state.goal_tasks,
        goal_total_estimated_time: state.goal_total_estimated_time,
      },
    });
  };

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
          <Button onClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">
            TOP画面へ
          </Button>
        </div>
      </div>
    </div>
  );
});
