import { useEffect, useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../../users/auth/useAuth";
import { updateGoalTasks } from "../api/goalTasksApi";
import type { TaskUpdateGeneratedData } from "../types/taskUpdateGeneratedData";

export const useTaskUpdateConfirm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { api } = useAuth();

  const generatedData = (location.state as TaskUpdateGeneratedData | null) ?? null;

  useEffect(() => {
    if (location.key === "default" || !generatedData?.form || !generatedData?.generated) {
      navigate("/tasks-update", { replace: true });
    }
  }, [location.key, navigate, generatedData?.form, generatedData?.generated]);

  const invalidState = location.key === "default" || !generatedData?.form || !generatedData?.generated;

  const formatDateForDisplay = (value: string) => value.replace(/-/g, "/");
  const items = useMemo(
    () =>
      (generatedData?.generated?.goalTasks ?? []).map((task) => ({
        value: `${formatDateForDisplay(task.deadline)} ${task.estimatedTime}分 ${task.goalTaskName}`,
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

  const handleUpdateGoalTasks = async () => {
    const toApiDate = (value: string) => value.replace(/\//g, "-");
    const payload = {
      goal: {
        goalName: generatedData?.form?.goal ?? "",
        statusAgainstGoal: generatedData?.form?.currentStatus ?? "",
        startDay: generatedData?.form?.startDate ? toApiDate(generatedData.form.startDate) : "",
        targetDay: generatedData?.form?.endDate ? toApiDate(generatedData.form.endDate) : "",
        weekdayAvailableTime: Number(generatedData?.form?.weekdayHours ?? 0),
        weekendsAvailableTime: Number(generatedData?.form?.holidayHours ?? 0),
        taskCreationRule: generatedData?.form?.conditions?.trim() || undefined,
      },
      goalTasks: generatedData?.generated?.goalTasks ?? [],
      goalTotalEstimatedTime: totalEstimatedTime,
    };

    try {
      await updateGoalTasks(api, payload);
      navigate("/top", { replace: true });
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (!err.response) {
          navigate("/server-connection-incomplete", {
            replace: true,
          });
          return;
        }
        navigate("/tasks-update/incomplete", {
          replace: true,
          state: {
            error: err.response?.data?.detail ?? "目標タスクの更新に失敗しました",
          },
        });
      } else {
        console.error("Unexpected error", err);
      }
    }
  };

  const handleNavigateToTop = () => {
    navigate("/tasks-update", {
      replace: true,
      state: {
        goalName: generatedData?.goalName,
        completedGoalTasks: generatedData?.completedGoalTasks,
        formValues: generatedData?.form,
      },
    });
  };

  return {
    invalidState,
    goalName,
    items,
    handleUpdateGoalTasks,
    handleNavigateToTop,
  };
};
