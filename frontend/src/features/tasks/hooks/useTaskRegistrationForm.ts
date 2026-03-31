import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../../users/auth/useAuth";
import type { TaskRegistrationFormType } from "../types/taskRegistrationForm";
import { generateGoalTasks } from "../api/goalTasksApi";

export const useTaskRegistrationForm = () => {
  const navigate = useNavigate();
  const { api } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmitRegistration = async (data: TaskRegistrationFormType) => {
    try {
      setIsLoading(true);
      const normalizeDateForApi = (value: string) => value.replace(/\//g, "-");
      const payload = {
        goal: {
          goalName: data.goal,
          statusAgainstGoal: data.currentStatus,
          startDay: normalizeDateForApi(data.startDate),
          targetDay: normalizeDateForApi(data.endDate),
          weekdayAvailableTime: Number(data.weekdayAvailableHours),
          weekendsAvailableTime: Number(data.holidayAvailableHours),
          taskCreationRule: data.conditions?.trim() || undefined,
        },
      };

      const generated = await generateGoalTasks(api, payload);
      navigate("/tasks-registration/confirm", {
        state: { form: data, generated },
        replace: true,
      });
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (!err.response) {
          navigate("/server-connection-incomplete", {
            replace: true,
          });
          return;
        }
        navigate("/tasks-generation/incomplete", {
          replace: true,
          state: {
            error: "目標タスクの生成に失敗しました",
          },
        });
      } else {
        console.error("Unexpected error", err);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleNavigateToTop = () => {
    navigate("/top", { replace: true });
  };

  return {
    isLoading,
    handleSubmitRegistration,
    handleNavigateToTop,
  };
};
