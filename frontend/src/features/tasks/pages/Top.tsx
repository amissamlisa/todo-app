import { memo } from "react";
import { Button } from "../../../shared/components/atoms/Button";
import { TwoButtonModal } from "../../../shared/components/molecules/TwoButtonModal";
import { IoWarning } from "react-icons/io5";
import KanbanBoard from "../../../shared/components/organism/KanbanBoard";
import { LogoutButton } from "../../../shared/components/atoms/LogoutButton";
import UserProfileIcon from "../../../assets/user-icon.png";
import { UserProfile } from "../../../shared/components/molecules/UserProfile";
import { List } from "../../../shared/components/molecules/List";
import Point from "../../../assets/point.png";
import WasteBasket from "../../../assets/waste-basket.png";
import { useTopPage } from "../hooks/useTopPage";
import CloudIcon from "../../assets/cloud.png";
import DropletIcon from "../../assets/droplet.png";
import GlowingCloudIcon from "../../assets/glowing-cloud.png";
import MistIcon from "../../assets/mist.png";

export const Top = memo(() => {
  const formatDateForDisplay = (value: string) => value.replace(/-/g, "/");
  const rankImageMap: Record<string, string> = {
    "雫": DropletIcon,
    "霧": MistIcon,
    "雲": CloudIcon,
    "光雲": GlowingCloudIcon,
  };
  const {
    activeModal,
    setActiveModal,
    showUserInfo,
    setShowUserInfo,
    showRankList,
    setShowRankList,
    topData,
    rankImage,
    todayTasks,
    goal,
    todoItems,
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
  } = useTopPage();

  return (
    <div className="min-h-screen overflow-y-auto bg-primary">
      <div className="flex items-center gap-3.75 mt-[clamp(18.5px,4.3vh,74px)] w-full pr-[clamp(7.5px,3.8vw,30px)]">
        <div className="relative ml-[clamp(7.5px,3.8vw,30px)]">
          <div className="relative flex flex-col items-center">
            <img
              src={UserProfileIcon}
              alt="User Profile"
              className="w-6.5 h-6.5 relative z-10"
              onClick={() => setShowUserInfo(true)}
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
            images={[rankImageMap["雫"], rankImageMap["霧"], rankImageMap["雲"], rankImageMap["光雲"]]}
            explanations={[
              "ポイント数:0pt～999pt\n世界を創造する一滴の雫。小さいながらも、可能性に満ち溢れた存在。",
              "ポイント数:1000pt～2999pt\nまだ形は定まっていないが、手探りで吸収しながら変化していく段階。",
              "ポイント数:3000pt～5999pt\n形が一定になり、安定して、無数の試練を乗り越えた確固たる存在へと成長した姿。",
              "ポイント数:6000pt～\nその光は、長い道のりを乗り越えた者だけが纏う証。成熟と輝きを宿した最上位の雲。",
            ]}
            titles={["雫", "霧", "雲", "光雲"]}
            showList={showRankList}
            setShowList={setShowRankList}
          />
        </div>
        <div className="relative flex flex-col items-center ml-3.75">
          <img
            src={rankImage}
            alt="User Rank"
            className="w-6.5 h-6.5 z-10 cursor-pointer"
            onClick={() => setShowRankList(true)}
          />
          <span className="absolute w-11.25 h-11.25 top-1/2 left-1/2  -translate-x-1/2 -translate-y-1/2   rounded-full bg-secondary z-0" />
        </div>
        <div className="flex items-center">
          <div className="flex  ml-2 items-center gap-1.5 px-1.5 py-1.5 rounded-md bg-secondary">
            <img src={Point} alt="User Points" className="w-8.25 h-8.25" />
            <p className="text-[#e8d464] whitespace-nowrap">{topData?.userPoints ?? 0}pt</p>
          </div>
        </div>
        <div className="ml-auto">
          <LogoutButton />
        </div>
      </div>
      <div className="flex flex-col items-center pb-6">
        <div className="flex items-center justify-center bg-secondary h-[clamp(35px,5.9vh,140px)] w-[clamp(178px,91.2vw,712px)] rounded-lg mt-2.5 mb-2.5">
          {goal ? (
            <div className="flex">
              <div>
                <h2 className="text-primary">期限: {goal?.targetDay ? formatDateForDisplay(goal.targetDay) : ""}</h2>
                <h2 className="text-primary">達成目標: {goal?.goalName}</h2>
              </div>
              <img
                src={WasteBasket}
                alt="Waste Basket"
                className="w-5 h-5 self-center mt-2 ml-2"
                onClick={handleOpenDeleteGoalModal}
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
            {todayTasks.map((task) => (
              <p key={task.goalTaskId} className="text-primary mt-1 wrap-break-word text-center">
                {task.goalTask}
              </p>
            ))}
          </div>
        </div>
        <div className="mt-[clamp(10px,2.4vh,40px)]">
          <KanbanBoard
            key={kanbanKey}
            TodoItems={todoItems}
            canAddTask={Boolean(goal)}
            onPointsChange={handlePointsChange}
            onDoneTasksChange={handleDoneTasksChange}
            onTodayTasksChange={handleTodayTasksChange}
          />
        </div>
        <Button onClick={() => setActiveModal("default")} buttonColor="bg-secondary" textColor="text-primary">
          {buttonText}
        </Button>
        <TwoButtonModal
          title={modalTitle1}
          isOpen={activeModal === "default"}
          content={modalButtonTitle}
          hasPartyPopper={false}
          hasTwoButtons={true}
          onClose={() => setActiveModal(null)}
          onClickChange={handleTaskPageNavigation}
        />
        <TwoButtonModal
          title={completeModalTitle}
          isOpen={activeModal === "complete"}
          content={completeModalContent}
          hasPartyPopper={true}
          hasTwoButtons={false}
          onClose={() => setActiveModal(null)}
          onClickChange={() => setActiveModal(null)}
        />
        <TwoButtonModal
          title="達成目標を削除"
          content="達成目標を削除すると、すべての達成目標タスクが削除されます。よろしいですか？"
          hasPartyPopper={false}
          hasTwoButtons={true}
          isOpen={activeModal === "deleteGoal"}
          onClose={() => setActiveModal(null)}
          onClickChange={handleDeleteGoalConfirm}
        />
        <TwoButtonModal
          title={rankUpModalTitle}
          isOpen={activeModal === "rankUp"}
          content={rankUpModalContent}
          hasPartyPopper={true}
          hasTwoButtons={false}
          onClose={() => setActiveModal(null)}
          onClickChange={() => setActiveModal(null)}
        />
      </div>
    </div>
  );
});