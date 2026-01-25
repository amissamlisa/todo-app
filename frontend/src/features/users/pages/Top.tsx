import { memo } from "react";
import { Button } from "../../../shared/components/atoms/Button";
import { useNavigate } from 'react-router-dom';
import { HeaderWithLogoutIcon } from "../../../shared/components/molecules/HeaderWithLogoutIcon";
import { useAuth } from "../auth/useAuth";


export const Top = memo(() => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const onButtonClick = () => {
    navigate("/", { replace: true });
  }
  const onLogoutClick = async () => {
    const isloggedOut = await logout();
    console.log(isloggedOut);
    if(isloggedOut === false){
      return null;
    }
    if (isloggedOut) {
      navigate("/logout", { replace: true });
      console.log("ログアウト成功");
    } 
   
    
  }

  return (
    <div className="overflow-y-auto h-screen ">
      <HeaderWithLogoutIcon onLogoutClick={onLogoutClick} />
      <div className="flex flex-col justify-center items-center mt-[clamp(37.5px,9.1vh,154px)]">
        <div className="mb-[clamp(251px,59.5vh,1006px)]">
          <Button onButtonClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">目標タスクを作成する</Button>
        </div>
      </div>
    </div>
  )
})