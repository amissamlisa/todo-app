import { memo, useEffect } from "react";
import { Header } from "../../../shared/components/molecules/Header";
import rainbowImg from "../../../assets/rainbow_cloud.png";
import { Button } from "../../../shared/components/atoms/Button";
import { useNavigate, useLocation } from 'react-router-dom';


export const PasswordResetMessageSent = memo(() => {
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
        <h2 className="text-primary mb-[clamp(9.5px,2.3vh,83px)] text-2xl">メールをご確認ください</h2>
        <h2 className="text-primary w-[clamp(134.5px,68.7vw,536px)]">入力されているメールアドレスが登録されている場合、パスワード再設定用のメールが送信されます。
        その場合メールに記載されているリンクから再設定をおこなってください。</h2>
        <img className=" w-[clamp(115px,59.2vw,462px)] " src={rainbowImg} />
        <div>
          <Button onClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">ログイン画面へ</Button>
        </div>
      </div>
    </div>
  )
})