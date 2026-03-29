import { useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../../users/auth/useAuth";
import { saveGoalTasks } from "../api/goalTasksApi";
import type { TaskRegistrationGeneratedData } from "../types/taskRegistrationGeneratedData";

export const useTaskRegistrationConfirm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { api } = useAuth();

  const generatedData = (location.state as TaskRegistrationGeneratedData | null) ?? null;

  const items = useMemo(
    () =>
      (generatedData?.generated?.goal_tasks ?? []).map((task) => ({
        value: `${task.deadline} ${task.estimated_time}分 ${task.goal_task_name}`,
      })),
    [generatedData?.generated?.goal_tasks]
  );

  const goalName = generatedData?.form?.goal ?? "";
  const totalEstimatedTime = useMemo(
    () =>
      (generatedData?.generated?.goal_tasks ?? []).reduce(
        (sum, task) => sum + task.estimated_time,
        0
      ),
    [generatedData?.generated?.goal_tasks]
  );

  const handleSaveGoalTasks = async () => {
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
        weekday_available_time: Number(generatedData?.form?.weekdayAvailableHours ?? 0),
        weekends_available_time: Number(generatedData?.form?.holidayAvailableHours ?? 0),
        task_creation_rule: generatedData?.form?.conditions?.trim() || undefined,
      },
      goal_tasks: generatedData?.generated?.goal_tasks ?? [],
      goal_total_estimated_time: totalEstimatedTime,
    };

    try {
      await saveGoalTasks(api, payload);
      navigate("/tasks-registration/complete", {
        replace: true,
        state: {
          goal: payload.goal,
          goal_tasks: payload.goal_tasks,
          goal_total_estimated_time: totalEstimatedTime,
        },
      });
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (!err.response) {
          navigate("/server-connection-incomplete", {
            replace: true,
          });
          return;
        }
        navigate("/tasks-registration/incomplete", {
          replace: true,
          state: {
            error: err.response?.data?.detail ?? "目標タスクの登録に失敗しました",
          },
        });
      } else {
        console.error("Unexpected error", err);
      }
    }
  };

  const handleNavigateRegistration = () => {
    navigate("/tasks-registration", { replace: true });
  };

  return {
    goalName,
    items,
    handleSaveGoalTasks,
    handleNavigateRegistration,
  };
};
