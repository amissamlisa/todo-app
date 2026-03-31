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
      (generatedData?.generated?.goalTasks ?? []).map((task) => ({
        value: `${task.deadline} ${task.estimatedTime}分 ${task.goalTaskName}`,
      })),
    [generatedData?.generated?.goalTasks]
  );

  const goalName = generatedData?.form?.goal ?? "";
  const totalEstimatedTime = useMemo(
    () =>
      (generatedData?.generated?.goalTasks ?? []).reduce(
        (sum, task) => sum + task.estimatedTime,
        0
      ),
    [generatedData?.generated?.goalTasks]
  );

  const handleSaveGoalTasks = async () => {
    const toApiDate = (value: string) => value.replace(/\//g, "-");
    const payload = {
      goal: {
        goalName: generatedData?.form?.goal ?? "",
        statusAgainstGoal: generatedData?.form?.currentStatus ?? "",
        startDay: generatedData?.form?.startDate
          ? toApiDate(generatedData.form.startDate)
          : "",
        targetDay: generatedData?.form?.endDate
          ? toApiDate(generatedData.form.endDate)
          : "",
        weekdayAvailableTime: Number(generatedData?.form?.weekdayAvailableHours ?? 0),
        weekendsAvailableTime: Number(generatedData?.form?.holidayAvailableHours ?? 0),
        taskCreationRule: generatedData?.form?.conditions?.trim() || undefined,
      },
      goalTasks: generatedData?.generated?.goalTasks ?? [],
      goalTotalEstimatedTime: totalEstimatedTime,
    };

    try {
      await saveGoalTasks(api, payload);
      navigate("/tasks-registration/complete", {
        replace: true,
        state: {
          goal: payload.goal,
          goalTasks: payload.goalTasks,
          goalTotalEstimatedTime: totalEstimatedTime,
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
