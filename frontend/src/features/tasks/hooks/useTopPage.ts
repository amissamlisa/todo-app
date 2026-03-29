import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import type { Cards } from "../../../shared/types/cards";
import { useAuth } from "../../users/auth/useAuth";
import type { TopData } from "../types/topData";
import { rankImageMap } from "../../../shared/types/rankImageMap";
import { deleteGoal as deleteGoalRequest, fetchTopData, updateTopPoints, updateTopRank } from "../api/topApi";

const RANK_ORDER: Record<string, number> = {
  "雫": 0,
  "霧": 1,
  "雲": 2,
  "光雲": 3,
};

type ModalType = "default" | "complete" | "rankUp" | "deleteGoal" | null;

export const useTopPage = () => {
  const navigate = useNavigate();
  const { token, api } = useAuth();

  const [activeModal, setActiveModal] = useState<ModalType>(null);
  const [showUserInfo, setShowUserInfo] = useState(false);
  const [showRankList, setShowRankList] = useState(false);
  const [hasTasks, setHasTasks] = useState(false);
  const [topData, setTopData] = useState<TopData | null>(null);
  const [rankUpTo, setRankUpTo] = useState(topData?.userRank ?? "雫");
  const [, setAllTasksCompleted] = useState(false);
  const [, setToday] = useState(new Date());
  const [todayTasks, setTodayTasks] = useState<Cards[]>([]);

  const rankImage = rankImageMap[topData?.userRank ?? "雫"] ?? rankImageMap["雫"];
  const path = hasTasks ? "/tasks-update" : "/tasks-registration";
  const goal = topData?.goal ?? null;
  const goalTasks = useMemo(() => topData?.goalTasks ?? [], [topData]);

  const navigateToServerConnectionIncomplete = useCallback(() => {
    navigate("/server-connection-incomplete", {
      replace: true,
    });
  }, [navigate]);

  const deleteGoal = useCallback(
    async (goalId: number) => {
      if (goalId <= 0 || !token) return false;
      try {
        await deleteGoalRequest(api, goalId);

        setTopData((previous) =>
          previous
            ? {
              ...previous,
              goal: null,
              goalTasks: [],
            }
            : previous
        );
        setHasTasks(false);
        setTodayTasks([]);
        setAllTasksCompleted(false);
        return true;
      } catch (err) {
        if (axios.isAxiosError(err) && !err.response) {
          navigateToServerConnectionIncomplete();
          return false;
        }
        console.error("Failed to delete goal and goal tasks", err);
        return false;
      }
    },
    [token, api, navigateToServerConnectionIncomplete]
  );

  const handleDeleteGoalConfirm = useCallback(async () => {
    const goalId = goal?.goal_id;
    if (!goalId) {
      setActiveModal(null);
      return;
    }

    const deleteResult = await deleteGoal(goalId);
    if (!deleteResult) return;
    setActiveModal(null);
  }, [goal, deleteGoal]);

  const handleOpenDeleteGoalModal = useCallback(() => {
    if (!goal?.goal_id) return;
    setActiveModal("deleteGoal");
  }, [goal]);

  const handlePointsChange = useCallback(
    async (points: number) => {
      if (!token || !topData) return;
      const nextPoints = Math.max(points, topData.userPoints);
      if (nextPoints === topData.userPoints) return;

      const rankByPoints = (value: number) => {
        if (value <= 999) return "雫";
        if (value <= 2999) return "霧";
        if (value <= 5999) return "雲";
        return "光雲";
      };

      try {
        await updateTopPoints(api, nextPoints);
        const nextRank = rankByPoints(nextPoints);
        if (nextRank !== topData.userRank) {
          await updateTopRank(api, nextRank);
        }

        setTopData((previous) => {
          if (!previous) return previous;

          if ((RANK_ORDER[nextRank] ?? 0) > (RANK_ORDER[previous.userRank] ?? 0)) {
            setRankUpTo(nextRank);
            setActiveModal("rankUp");
          }

          return {
            ...previous,
            userPoints: nextPoints,
            userRank: nextRank,
          };
        });
      } catch (err) {
        if (axios.isAxiosError(err) && !err.response) {
          navigateToServerConnectionIncomplete();
          return;
        }
        console.error("update points failed", err);
      }
    },
    [token, topData, api, navigateToServerConnectionIncomplete]
  );

  const handleDoneTasksChange = useCallback((todoItems: Cards[], inProgressItems: Cards[], doneItems: Cards[]) => {
    const allDone =
      todoItems.length === 0 &&
      inProgressItems.length === 0 &&
      doneItems.length > 0;

    if (allDone) {
      setAllTasksCompleted((previous) => {
        if (previous) return previous;
        setActiveModal("complete");
        return true;
      });
      return;
    }
    setActiveModal((previous) => (previous ? null : previous));
  }, []);

  const handleTodayTasksChange = useCallback((todoItems: Cards[], inProgressItems: Cards[]) => {
    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, "0");
    const day = today.getDate().toString().padStart(2, "0");
    const targetDate = `${year}-${month}-${day}`;

    const nextTodayTasks = [
      ...todoItems.filter((task) => task.deadline === targetDate),
      ...inProgressItems.filter((task) => task.deadline === targetDate),
    ];

    setTodayTasks((previous) => {
      const previousKey = previous
        .map((task) => `${task.goal_task_id}:${task.deadline}:${task.goal_task_status}`)
        .join("|");
      const nextKey = nextTodayTasks
        .map((task) => `${task.goal_task_id}:${task.deadline}:${task.goal_task_status}`)
        .join("|");

      return previousKey === nextKey ? previous : nextTodayTasks;
    });
  }, []);

  useEffect(() => {
    const msUntilMidnight = () => {
      const now = new Date();
      const midnight = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() + 1
      );
      return midnight.getTime() - now.getTime();
    };

    let intervalId: ReturnType<typeof setInterval> | null = null;
    const timeout = setTimeout(() => {
      setToday(new Date());
      intervalId = setInterval(() => {
        setToday(new Date());
      }, 86400000);
    }, msUntilMidnight());

    return () => {
      clearTimeout(timeout);
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, []);

  useEffect(() => {
    if (!token) return;

    const fetchTop = async () => {
      try {
        const nextTopData = await fetchTopData(api);
        setTopData(nextTopData);
        setHasTasks(nextTopData.goalTasks.length > 0);
      } catch (err) {
        if (axios.isAxiosError(err) && !err.response) {
          navigateToServerConnectionIncomplete();
          return;
        }
        console.error(err);
      }
    };

    fetchTop();
  }, [token, api, navigateToServerConnectionIncomplete]);

  const handleTaskPageNavigation = useCallback(() => {
    if (path === "/tasks-update") {
      const completedGoalTasks = goalTasks
        .filter((task) => task.goal_task_status === "完了")
        .map((task) => ({
          goal_task_name: task.goal_task_name,
          deadline: task.deadline,
          estimated_time: task.estimated_time,
        }));

      navigate(path, {
        replace: true,
        state: {
          goalName: goal?.goal_name ?? "",
          completedGoalTasks,
        },
      });
      return;
    }

    navigate(path, { replace: true });
  }, [path, goalTasks, navigate, goal]);


  const todoItems: Cards[] = useMemo(
    () =>
      goalTasks.map((task, index) => ({
        goal_task_id: task.goal_task_id ?? index + 1,
        order_num: task.order_num ?? index + 1,
        goal_task_status: task.goal_task_status,
        goal_task: task.goal_task_name,
        time: task.estimated_time,
        deadline: task.deadline,
      })),
    [goalTasks]
  );

  const kanbanKey = useMemo(
    () =>
      goalTasks
        .map((task) => `${task.goal_task_id}:${task.order_num}:${task.goal_task_status}`)
        .join("|"),
    [goalTasks]
  );

  const buttonText = hasTasks ? "目標タスクを更新する" : "目標タスクを作成する";
  const modalButtonTitle = hasTasks
    ? "目標タスクを更新しますか？"
    : "目標タスクを作成しますか";
  const modalTitle1 = hasTasks ? "目標タスクを更新" : "目標タスクを作成";
  const completeModalTitle = "目標タスク完了";
  const completeModalContent = "おめでとうございます\n目標タスクがすべて完了しました!!!\n";
  const rankUpModalTitle = "ランクアップ";
  const rankUpModalContent = `おめでとうございます\n${rankUpTo}にランクアップしました!!!`;

  return {
    activeModal,
    setActiveModal,
    showUserInfo,
    setShowUserInfo,
    showRankList,
    setShowRankList,
    topData,
    rankImage,
    todayTasks,
    todoItems,
    goal,
    goalTasks,
    kanbanKey,
    buttonText,
    modalButtonTitle,
    modalTitle1,
    completeModalTitle,
    completeModalContent,
    rankUpModalTitle,
    rankUpModalContent,
    handleTaskPageNavigation,
    handleOpenDeleteGoalModal,
    handleDeleteGoalConfirm,
    handlePointsChange,
    handleDoneTasksChange,
    handleTodayTasksChange,
  };
};
