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
    navigate("/", {replace: true});
  }

  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="flex flex-col justify-center items-center mt-[clamp(68.5px,16.2vh,274px)]">
        <h2 className="text-primary">{errMessage}</h2>
        <img className=" w-[clamp(115px,59.2vw,462px)] " src={rainCloudImg} />
        <div className="mb-[clamp(251px,59.5vh,1006px)]">  
        <Button onButtonClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">ログイン画面へ</Button>
        </div>
      </div>
    </div>
  )
})