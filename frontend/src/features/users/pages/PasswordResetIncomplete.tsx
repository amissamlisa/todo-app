import { memo, useEffect } from "react";
import { Header } from "../../../shared/components/molecules/Header";
import rainCloudImg from "../../../assets/rain-cloud.png";
import { Button } from "../../../shared/components/atoms/Button";
import { useNavigate, useLocation } from "react-router-dom";

export const PasswordResetIncomplete = memo(() => {
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
      <div className="flex flex-col justify-center items-center mt-[clamp(37.5px,9.1vh,154px)]">
        <h2 className="text-primary mb-[clamp(27.5px,6.5vh,110px)] text-2xl">パスワード再設定失敗</h2>
        <h2 className="text-primary w-[clamp(112.5px,57.6vw,450px)]">申し訳ございません。パスワード再設定リンクが無効です。再度、リンクを発行しなおしてください</h2>
        <img className=" w-[clamp(115px,59.2vw,462px)] " src={rainCloudImg} />
        <div className="mb-[clamp(251px,59.5vh,1006px)]">
          <Button onButtonClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">ログイン画面へ</Button>
        </div>
      </div>
    </div>
  )
})