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
      (generatedData?.generated?.goal_tasks ?? []).map((task) => ({
        value: `${formatDateForDisplay(task.deadline)} ${task.estimated_time}分 ${task.goal_task_name}`,
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

  const handleUpdateGoalTasks = async () => {
    const toApiDate = (value: string) => value.replace(/\//g, "-");
    const payload = {
      goal: {
        goal_name: generatedData?.form?.goal ?? "",
        status_against_goal: generatedData?.form?.currentStatus ?? "",
        start_day: generatedData?.form?.startDate ? toApiDate(generatedData.form.startDate) : "",
        target_day: generatedData?.form?.endDate ? toApiDate(generatedData.form.endDate) : "",
        weekday_available_time: Number(generatedData?.form?.weekdayHours ?? 0),
        weekends_available_time: Number(generatedData?.form?.holidayHours ?? 0),
        task_creation_rule: generatedData?.form?.conditions?.trim() || undefined,
      },
      goal_tasks: generatedData?.generated?.goal_tasks ?? [],
      goal_total_estimated_time: totalEstimatedTime,
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
    navigate("/tasks-update", { replace: true });
  };

  return {
    invalidState,
    goalName,
    items,
    handleUpdateGoalTasks,
    handleNavigateToTop,
  };
};
