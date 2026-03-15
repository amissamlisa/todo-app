import { ImCross } from "react-icons/im";
import UserProfileIcon from "../../../assets/user_icon.png";
import UserProfileProps from "../types/userProfile";

export const UserProfile = ({
  showUserInfo,
  username,
  email,
  setShowUserInfo
}: UserProfileProps) => {

  if (!showUserInfo) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/70 flex items-start justify-start">
      <div className="relative z-60 h-[clamp(297.5px,70.4vh,1190px)] w-[clamp(147.5px,75.4vw,590px)] bg-secondary rounded-r-lg shadow-lg p-4 pt-[clamp(25px,5.9vh,100px)]]">
        <ImCross
          className="absolute top-10 right-5 cursor-pointer text-primary"
          onClick={() => setShowUserInfo(false)}
        />
        <div className="flex flex-col items-center">
          <h2 className="text-primary text-lg font-bold">ユーザー情報</h2>
          <img
            src={UserProfileIcon}
            alt="User Profile"
            className="w-20 h-20 relative z-10"
          />
          <span className="absolute w-20 h-20 border-primary top-1/2 left-1/2  -translate-x-1/2 -translate-y-1/2 rounded-full z-0" />
        </div>
        <div className="text-primary flex flex-col mb-[clamp(16.5px,8.4vh,66px)] mt-[clamp(9.5px,2.2vh,38px)] items-start">
          <p>ユーザー名 {username}</p>
          <p>メールアドレス {email}</p>
        </div>
      </div>
    </div>
  );
};