import { memo, useCallback, useEffect, useMemo, useState } from "react";
import { Button } from "../../../shared/components/atoms/Button";
import { useNavigate } from "react-router-dom";
import { TwoButtonModal } from "../../../shared/components/molecules/TwoButtonModal";
import { IoWarning } from "react-icons/io5";
import KanbanBoard from "../../../shared/components/organism/KanbanBoard";
import type { Cards } from "../../../shared/types/cards";
import { useAuth } from "../../users/auth/useAuth";
import { LogoutButton } from "../../../shared/components/atoms/LogoutButton";
import UserProfileIcon from "../../../assets/user-icon.png";
import { UserProfile } from "../../../shared/components/molecules/UserProfile";
import { List } from "../../../shared/components/molecules/List";
import CloudIcon from "../../../assets/cloud.png";
import DropletIcon from "../../../assets/droplet.png";
import GlowingCloudIcon from "../../../assets/glowing-cloud.png";
import MistIcon from "../../../assets/mist.png";
import Point from "../../../assets/point.png";
import WasteBasket from "../../../assets/waste-basket.png";
import type { TopGoalTask } from "../../tasks/types/topGaolTask";
import type { TopGoal } from "../../tasks/types/topGoal";
import axios from "axios";

const RANK_ORDER: Record<string, number> = {
  "雫": 0,
  "霧": 1,
  "雲": 2,
  "光雲": 3,
};
export const Top = memo(() => {
  const navigate = useNavigate();

  const openUserInfo = () => {
    setShowUserInfo(true);
  };
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isCompleteModalOpen, setIsCompleteModalOpen] = useState(false);
  const [isRankUpModalOpen, setIsRankUpModalOpen] = useState(false);
  const [isDeleteGoalModalOpen, setIsDeleteGoalModalOpen] = useState(false);

  const [showUserInfo, setShowUserInfo] = useState(false);
  const [showList, setShowList] = useState(false);
  const [canGetTask, setCanGetTask] = useState(false);

  const [topData, setTopData] = useState<{
    username: string;
    email: string;
    user_rank: string;
    user_points: number;
    goal: TopGoal | null;
    goal_tasks: TopGoalTask[];
  } | null>(null);
  const [rankUpTo, setRankUpTo] = useState(topData?.user_rank ?? "雫");
  const rankImageMap: Record<string, string> = {
    "雫": DropletIcon,
    "霧": MistIcon,
    "雲": CloudIcon,
    "光雲": GlowingCloudIcon,
  };
  const rankImage = rankImageMap[topData?.user_rank ?? "雫"] ?? DropletIcon;
  const { token, api } = useAuth();

  const navigateToServerConnectionIncomplete = useCallback(() => {
    navigate("/server-connection-incomplete", {
      replace: true,
    });
  }, [navigate]);

  const onDeleteGoalsAndGoalTasks = async (goal_id: number) => {
    if (!token || goal_id <= 0) return false;
    try {
      await api.delete(`/goal/${goal_id}`);

      setTopData((previous) =>
        previous
          ? {
            ...previous,
            goal: null,
            goal_tasks: [],
          }
          : previous
      );
      setCanGetTask(false);
      setTomorrowTasks([]);
      setHasOpened(false);
      return true;
    } catch (err) {
      if (axios.isAxiosError(err) && !err.response) {
        navigateToServerConnectionIncomplete();
        return false;
      }
      console.error("Failed to delete goal and goal tasks", err);
      return false;
    }
  };

  const onOpenDeleteGoalModal = () => {
    if (!displayGoal?.goal_id) return;
    setIsDeleteGoalModalOpen(true);
  };

  const onConfirmDeleteGoal = async () => {
    const goalId = displayGoal?.goal_id;
    if (!goalId) {
      setIsDeleteGoalModalOpen(false);
      return;
    }

    const isDeleted = await onDeleteGoalsAndGoalTasks(goalId);
    if (!isDeleted) return;
    setIsDeleteGoalModalOpen(false);
  };
  const onKanbanPointsChange = useCallback(
    async (points: number) => {
      if (!token || !topData) return;
      const nextPoints = Math.max(points, topData.user_points);
      if (nextPoints === topData.user_points) return;
      const rankByPoints = (value: number) => {
        if (value <= 999) return "雫";
        if (value <= 2999) return "霧";
        if (value <= 5999) return "雲";
        return "光雲";
      };
      const payload = {
        points: nextPoints,
      };
      try {
        await api.put(`/top/points`, payload);
        const nextRank = rankByPoints(nextPoints);

        if (nextRank !== topData.user_rank) {
          await api.put(`/top/rank`, { user_rank: nextRank });
        }

        setTopData((previous) => {
          if (!previous) return previous;

          if ((RANK_ORDER[nextRank] ?? 0) > (RANK_ORDER[previous.user_rank] ?? 0)) {
            setRankUpTo(nextRank);
            setIsRankUpModalOpen(true);
          }

          return {
            ...previous,
            user_points: nextPoints,
            user_rank: nextRank,
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
    [token, topData, api, navigateToServerConnectionIncomplete, setRankUpTo, setIsRankUpModalOpen]
  );

  const [, setHasOpened] = useState(false);
  const onDoneTasksChange = (todoItems: Cards[], inProgressItems: Cards[], doneItems: Cards[]) => {
    const allDone =
      todoItems.length === 0 &&
      inProgressItems.length === 0 &&
      doneItems.length > 0;

    if (allDone) {
      setHasOpened((previous) => {
        if (previous) return previous;
        setIsCompleteModalOpen(true);
        return true;
      });
      return;
    }

    setIsCompleteModalOpen((previous) => (previous ? false : previous));
  };


  const [, setToday] = useState(new Date());
  const [tomorrowTasks, setTomorrowTasks] = useState<Cards[]>([]);
  const onTomorrowTasksChange = (todoItems: Cards[], inProgressItems: Cards[]) => {

    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, "0");
    const day = today.getDate().toString().padStart(2, "0");
    const targetDate = `${year}-${month}-${day}`;

    const nextTomorrowTasks = [
      ...todoItems.filter((task) => task.deadline === targetDate),
      ...inProgressItems.filter((task) => task.deadline === targetDate),
    ];

    setTomorrowTasks((previous) => {
      const previousKey = previous
        .map((task) => `${task.goal_task_id}:${task.deadline}:${task.goal_task_status}`)
        .join("|");
      const nextKey = nextTomorrowTasks
        .map((task) => `${task.goal_task_id}:${task.deadline}:${task.goal_task_status}`)
        .join("|");

      return previousKey === nextKey ? previous : nextTomorrowTasks;
    });
  };

  useEffect(() => {

    function msUntilMidnight() {
      const now = new Date();
      const midnight = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() + 1
      );
      return midnight.getTime() - now.getTime();
    }

    const timeout = setTimeout(() => {
      setToday(new Date());

      setInterval(() => {
        setToday(new Date());
      }, 86400000);

    }, msUntilMidnight());

    return () => clearTimeout(timeout);

  }, []);


  const path = canGetTask ? "/tasks-update" : "/tasks-registration";
  const displayGoal = topData?.goal ?? null;
  const displayGoalTasks = useMemo(() => topData?.goal_tasks ?? [], [topData]);
  const onClickChange = () => {
    if (path === "/tasks-update") {
      const completedGoalTasks = displayGoalTasks
        .filter((task) => task.goal_task_status === "完了")
        .map((task) => ({
          goal_task_name: task.goal_task_name,
          deadline: task.deadline,
          estimated_time: task.estimated_time,
        }));

      navigate(path, {
        replace: true,
        state: {
          goalName: displayGoal?.goal_name ?? "",
          completedGoalTasks,
        },
      });
      return;
    }
    navigate(path, { replace: true });
  };
  const buttonText = canGetTask ? "目標タスクを更新する" : "目標タスクを作成する";
  const isOpenModal = () => {
    setIsModalOpen(true);
  };





  const TodoItems: Cards[] = useMemo(
    () =>
      displayGoalTasks.map((task: TopGoalTask, index: number) => ({
        goal_task_id: task.goal_task_id ?? index + 1,
        order_num: task.order_num ?? index + 1,
        goal_task_status: task.goal_task_status,
        goal_task: task.goal_task_name,
        time: task.estimated_time,
        deadline: task.deadline,
      })),
    [displayGoalTasks]
  );

  const kanbanKey = useMemo(
    () =>
      displayGoalTasks
        .map((task) => `${task.goal_task_id}:${task.order_num}:${task.goal_task_status}`)
        .join("|"),
    [displayGoalTasks]
  );

  useEffect(() => {
    if (!token) return;
    const fetchTop = async () => {
      try {
        const response = await api.get(`/top`);
        setTopData(response.data);
        if (response.data.goal_tasks && response.data.goal_tasks.length > 0) {
          setCanGetTask(true);
        } else {
          setCanGetTask(false);
        }
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

  const modalButtonTitle = canGetTask
    ? "目標タスクを更新しますか？"
    : "目標タスクを作成しますか";
  const completeModalTitle = "目標タスク完了";
  const completeModalContent = "おめでとうございます\n目標タスクがすべて完了しました!!!\n";
  const rankUpModalTitle = "ランクアップ";
  const rankUpModalContent = `おめでとうございます\n${rankUpTo}にランクアップしました!!!`;

  const modalTitle1 = canGetTask ? "目標タスクを更新" : "目標タスクを作成";
  const handleClick = canGetTask ? isOpenModal : isOpenModal;

  return (
    <div className="min-h-screen overflow-y-auto bg-primary">
      <div className="flex items-center gap-3.75 mt-[clamp(18.5px,4.3vh,74px)] w-full pr-[clamp(7.5px,3.8vw,30px)]">
        <div className="relative ml-[clamp(7.5px,3.8vw,30px)]">
          <div className="relative flex flex-col items-center">
            <img
              src={UserProfileIcon}
              alt="User Profile"
              className="w-6.5 h-6.5 relative z-10"
              onClick={openUserInfo}
            />
            <span className="absolute w-11.25 h-11.25 top-1/2 left-1/2  -translate-x-1/2 -translate-y-1/2   rounded-full bg-secondary z-0" />
          </div>
          <UserProfile
            username={topData?.username ?? ""}
            email={topData?.email ?? ""}
            showUserInfo={showUserInfo}
            setShowUserInfo={setShowUserInfo}
          />
          <List
            mainTitle="ランク説明"
            images={[DropletIcon, MistIcon, CloudIcon, GlowingCloudIcon]}
            explanations={[
              "ポイント数:0pt～999pt\n世界を創造する一滴の雫。小さいながらも、可能性に満ち溢れた存在。",
              "ポイント数:1000pt～2999pt\nまだ形は定まっていないが、手探りで吸収しながら変化していく段階。",
              "ポイント数:3000pt～5999pt\n形が一定になり、安定して、無数の試練を乗り越えた確固たる存在へと成長した姿。",
              "ポイント数:6000pt～\nその光は、長い道のりを乗り越えた者だけが纏う証。成熟と輝きを宿した最上位の雲。",
            ]}
            titles={["雫", "霧", "雲", "光雲"]}
            showList={showList}
            setShowList={setShowList}
          />
        </div>
        <div className="relative flex flex-col items-center ml-3.75">
          <img
            src={rankImage}
            alt="User Rank"
            className="w-6.5 h-6.5 z-10 cursor-pointer"
            onClick={() => setShowList(true)}
          />
          <span className="absolute w-11.25 h-11.25 top-1/2 left-1/2  -translate-x-1/2 -translate-y-1/2   rounded-full bg-secondary z-0" />
        </div>
        <div className="flex items-center">
          <div className="flex  ml-2 items-center gap-1.5 px-1.5 py-1.5 rounded-md bg-secondary">
            <img src={Point} alt="User Points" className="w-8.25 h-8.25" />
            <p className="text-[#e8d464] whitespace-nowrap">{topData?.user_points ?? 0}pt</p>
          </div>
        </div>
        <div className="ml-auto">
          <LogoutButton />
        </div>
      </div>
      <div className="flex flex-col items-center pb-6">
        <div className="flex items-center justify-center bg-secondary h-[clamp(35px,5.9vh,140px)] w-[clamp(178px,91.2vw,712px)] rounded-lg mt-2.5 mb-2.5">

          {displayGoal ? (
            <div className="flex">
              <div>
                <h2 className="text-primary">期限: {displayGoal?.target_day}</h2>
                <h2 className="text-primary">達成目標: {displayGoal?.goal_name}</h2>
              </div>
              <img
                src={WasteBasket}
                alt="Waste Basket"
                className="w-5 h-5 self-center mt-2 ml-2"
                onClick={onOpenDeleteGoalModal}
              />
            </div>
          ) : (
            <div className="text-primary self-start">達成目標</div>
          )}

        </div>
        <div className="bg-secondary h-[clamp(35px,6vh,140px)] w-[clamp(178px,91.2vw,712px)] rounded-lg">
          <div className="flex flex-col h-full overflow-y-auto overflow-x-hidden px-3 py-2">
            <div className="flex items-center justify-center">
              <IoWarning className="text-[#ff8f8f]" />
              <p className="text-primary self-start">今日までのタスク</p>
            </div>
            {tomorrowTasks.map((task) => (
              <p key={task.goal_task_id} className="text-primary mt-1 wrap-break-word text-center">
                {task.goal_task}
              </p>
            ))}
          </div>
        </div>
        <div className="mt-[clamp(10px,2.4vh,40px)]">
          <KanbanBoard
            key={kanbanKey}
            TodoItems={TodoItems}
            isAddTaskEnabled={Boolean(displayGoal)}
            onPointsChange={onKanbanPointsChange}
            onDoneTasksChange={onDoneTasksChange}
            onTomorrowTasksChange={onTomorrowTasksChange}
          />
        </div>
        <Button onClick={handleClick} buttonColor="bg-secondary" textColor="text-primary">
          {buttonText}
        </Button>
        <TwoButtonModal
          title={modalTitle1}
          showFlag={isModalOpen}
          content={modalButtonTitle}
          hasPartyPopper={false}
          hasTwoButtons={true}
          setIsOpenModal={setIsModalOpen}
          onClickChange={onClickChange}
        />
        <TwoButtonModal
          title={completeModalTitle}
          showFlag={isCompleteModalOpen}
          content={completeModalContent}
          hasPartyPopper={true}
          hasTwoButtons={false}
          setIsOpenModal={setIsCompleteModalOpen}
          onClickChange={() => setIsCompleteModalOpen(false)}
        />
        <TwoButtonModal
          title="達成目標を削除"
          content="達成目標を削除すると、すべての達成目標タスクが削除されます。よろしいですか？"
          hasPartyPopper={false}
          hasTwoButtons={true}
          showFlag={isDeleteGoalModalOpen}
          setIsOpenModal={setIsDeleteGoalModalOpen}
          onClickChange={onConfirmDeleteGoal}
        />
        <TwoButtonModal
          title={rankUpModalTitle}
          showFlag={isRankUpModalOpen}
          content={rankUpModalContent}
          hasPartyPopper={true}
          hasTwoButtons={false}
          setIsOpenModal={setIsRankUpModalOpen}
          onClickChange={() => setIsRankUpModalOpen(false)}
        />
      </div>
    </div>
  );
});