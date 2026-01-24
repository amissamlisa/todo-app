import { memo } from "react";
import { Header } from "../../../shared/components/molecules/Header";
import rainCloudImg from "../../../assets/rain-cloud.png";
import { Button } from "../../../shared/components/atoms/Button";
import { useLocation, useNavigate } from 'react-router-dom';


export const AccountRegistrationIncomplete = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();
  const errMessage = location.state.error;
  const onButtonClick = () => {
    navigate("/", { replace: true });
  }

  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="flex flex-col justify-center items-center">
        <h2 className="text-primary mt-[clamp(15px,9.1vh,60px)] mb-[clamp(20px,4.7vh,80px)] text-2xl">アカウント登録失敗</h2>
        <h2 className="text-primary">{errMessage}</h2>
        <img className=" w-[clamp(115px,59.2vw,462px)] " src={rainCloudImg} />
        <div className="mb-[clamp(251px,59.5vh,1006px)]">
          <Button onButtonClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">ログイン画面へ</Button>
        </div>
      </div>
    </div>
  )
})