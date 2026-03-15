import { memo, useEffect } from "react";
import { Header } from "../../../shared/components/molecules/Header";
import rainbowImg from "../../../assets/rainbow_cloud.png";
import { Button } from "../../../shared/components/atoms/Button";
import { useNavigate, useLocation } from 'react-router-dom';


export const AccountRegistrationComplete = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.key === 'default') {
      navigate("/", { replace: true });
    }
  }, [location.key, navigate]);

  if (location.key === 'default') {
    return null;
  }

  const onButtonClick = () => {
    navigate("/", { replace: true });
  }

  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="flex flex-col justify-center items-center">
        <h2 className="text-primary mt-[clamp(15px,9.1vh,60px)] mb-[clamp(20px,4.7vh,80px)] text-2xl">アカウント登録完了</h2>
        <h2 className="text-primary">アカウント登録完了しました</h2>
        <img className=" w-[clamp(115px,59.2vw,462px)] " src={rainbowImg} />
        <div>
          <Button onClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">ログイン画面へ</Button>
        </div>
      </div>
    </div>
  )
})