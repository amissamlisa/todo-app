import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import type { TaskRegistrationCompleteState } from "../types/taskRegistrationComplete";

export const useTaskRegistrationComplete = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const state = (location.state as TaskRegistrationCompleteState | null) ?? null;
  const invalidState = location.key === "default" || !state?.goal || !state?.goalTasks;
  useEffect(() => {
    if (invalidState) {
      navigate("/tasks-registration", { replace: true });
    }
  }, [invalidState, navigate]);

  const handleMoveTop = () => {
    navigate("/top", {
      replace: true,
      state: {
        goal: state?.goal,
        goalTasks: state?.goalTasks,
        goalTotalEstimatedTime: state?.goalTotalEstimatedTime,
      },
    });
  };

  return {
    invalidState,
    handleMoveTop,
  };
};
