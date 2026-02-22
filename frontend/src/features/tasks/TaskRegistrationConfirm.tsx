import { memo } from "react";
import { RegistrationConfirmForm } from "../../shared/components/molecules/RegistrationConfirmForm";
import { useLocation, useNavigate } from "react-router-dom";
import { HeaderWithLogoutIcon } from "../../shared/components/molecules/HeaderWithLogoutIcon";
import { TwoButton } from "../../shared/components/molecules/TwoButton";
import { useAuth } from "../users/auth/useAuth";
import axios from "axios";

export const TaskRegistrationConfirm = memo(
  () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { token } = useAuth();
    const generatedData = location.state as {
      form?: {
        goal: string;
        currentStatus: string;
        startDate: string;
        endDate: string;
        weekdayHours: string;
        holidayHours: string;
        conditions: string;
        total_estimated_time?: number;
      };
      generated?: {
        goal_tasks?: {
          goal_task_name: string;
          deadline: string;
          estimated_time: number;
        }[];
      };
    } | null;

    const items = (generatedData?.generated?.goal_tasks ?? []).map((task) => ({
      value: `${task.deadline} ${task.estimated_time}分 ${task.goal_task_name}`,
    }));

    const goalName = generatedData?.form?.goal ?? "";
    let total_estimated_time = 0;
    for (const task of generatedData?.generated?.goal_tasks ?? []) {
      total_estimated_time += task.estimated_time;
    }
    const onPrimaryClick = async () => {
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
      const toApiDate = (value: string) => value.replace(/\//g, "-");
      const payload = {
        goal: {
          goal_name: generatedData?.form?.goal ?? "",
          status_against_goal: generatedData?.form?.currentStatus ?? "",
          start_day: generatedData?.form?.startDate
            ? toApiDate(generatedData.form.startDate)
            : "",
          target_day: generatedData?.form?.endDate
            ? toApiDate(generatedData.form.endDate)
            : "",
          weekday_available_time: Number(generatedData?.form?.weekdayHours ?? 0),
          weekends_available_time: Number(generatedData?.form?.holidayHours ?? 0),
          task_creation_rule: generatedData?.form?.conditions?.trim() || undefined,
        },
        goal_tasks: generatedData?.generated?.goal_tasks ?? [],
        goal_total_estimated_time: total_estimated_time,
      };
      try {
        console.log("/goal_tasks/save payload", payload);
        await axios.post(
          `${API_BASE_URL}/goal_tasks/save`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }

        );
        navigate("/tasks-registration/complete", {
          replace: true,
          state: {
            goal: payload.goal,
            goal_tasks: payload.goal_tasks,
            goal_total_estimated_time: total_estimated_time
          },
        });
      } catch (err) {
        if (axios.isAxiosError(err)) {
          console.error("/goal_tasks/save error", err.response?.data);
          console.error(err.response?.data?.detail ?? "目標タスクの登録に失敗しました");
          navigate("/tasks-registration/incomplete", { replace: true, });
        } else {
          console.error("予期しないエラー", err);
        }
      }
    };
    const onSecondaryClick = () => {
      navigate("/tasks-registration", { replace: true });
    }

    return (
      <div className="overflow-y-auto h-screen">
        <HeaderWithLogoutIcon />
        <div className="bg-secondary flex flex-col items-center ">
          <p className={`text-primary font-bold text-center mt-[clamp(14px,3.3vh,56px)] mb-[clamp(7px,1.6vh,28px)]`}>達成目標</p>
          <div className={`text-secondary bg-primary rounded-[5px] overflow-y-auto pl-[4vw] pr-[4vw] h-[clamp(25px,5.9vh,100px)] w-[clamp(163.5px,84vw,654px)] mb-[clamp(10.5px,2.4vh,42px)] flex items-center justify-center text-center`}>
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
            <TwoButton buttonTitle1="登録" buttonTitle2="戻る" buttonBgColor="bg-primary" buttonTextColor="text-secondary" onPrimaryClick={onPrimaryClick} onSecondaryClick={onSecondaryClick} />
          </div>
        </div>
      </div>
    );
  }
);