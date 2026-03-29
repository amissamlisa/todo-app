import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../../users/auth/useAuth";
import { generateGoalTasks } from "../api/goalTasksApi";
import type { TaskUpdateFormType, TaskUpdateLocationState } from "../types/taskUpdateForm";

export const useTaskUpdateForm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { api } = useAuth();

  const [isLoading, setIsLoading] = useState(false);
  const state = (location.state as TaskUpdateLocationState | null) ?? null;
  const goalName = state?.goalName ?? "";
  const completedGoalTasks = state?.completedGoalTasks ?? [];

  const handleUpdateGoalTasks = async (data: TaskUpdateFormType) => {
    try {
      setIsLoading(true);
      const toApiDate = (value: string) => value.replace(/\//g, "-");
      const payload = {
        goal: {
          goal_name: goalName,
          status_against_goal: data.currentStatus,
          start_day: toApiDate(data.startDate),
          target_day: toApiDate(data.endDate),
          weekday_available_time: Number(data.weekdayHours),
          weekends_available_time: Number(data.holidayHours),
          task_creation_rule: data.conditions?.trim() || undefined,
        },
        completed_goal_tasks_list: completedGoalTasks,
      };

      const generated = await generateGoalTasks(api, payload);
      navigate("/tasks-update/confirm", {
        state: { form: data, generated },
        replace: true,
      });
    } catch (err) {
      if (axios.isAxiosError(err) && !err.response) {
        navigate("/server-connection-incomplete", {
          replace: true,
        });
      } else {
        navigate("/tasks-generation/incomplete", {
          replace: true,
          state: {
            error: "目標タスクの生成に失敗しました",
          },
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleNavigateTop = () => {
    navigate("/top", { replace: true });
  };

  const handleNavigateToTopWhenGoalMissing = () => {
    if (!goalName) {
      navigate("/top", { replace: true });
      return true;
    }
    return false;
  };

  return {
    isLoading,
    goalName,
    handleUpdateGoalTasks,
    handleNavigateTop,
    handleNavigateToTopWhenGoalMissing,
  };
};
