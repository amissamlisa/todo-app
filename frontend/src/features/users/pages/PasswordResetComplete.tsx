import { memo } from "react";
import { Header } from "../../../shared/components/molecules/Header";
import rainbowImg from "../../../assets/rainbow.png";
import { useNavigate } from "react-router-dom";
import { Button } from "../../../shared/components/atoms/Button";

export const PasswordResetComplete = memo(() => {
  const navigate = useNavigate();

  const onButtonClick = () => {
    navigate("/", { replace: true });
  }
  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="flex flex-col justify-center items-center mt-[clamp(37.5px,9.1vh,154px)]">
        <h2 className="text-primary mb-[clamp(27.5px,6.5vh,110px)] text-2xl">パスワード再設定完了</h2>
        <h2 className="text-primary w-[clamp(112.5px,57.6vw,450px)]">パスワード再設定が完了しました。ログイン時は新しいパスワードを使用してください</h2>
        <img className=" w-[clamp(115px,59.2vw,462px)] " src={rainbowImg} />
        <div className="mb-[clamp(251px,59.5vh,1006px)]">
          <Button onClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">ログイン画面へ</Button>
        </div>
      </div>
    </div>
  )
})