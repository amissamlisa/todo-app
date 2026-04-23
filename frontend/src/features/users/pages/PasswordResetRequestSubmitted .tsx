import { memo } from "react";
import { Header } from "../../../shared/components/molecules/Header";
import rainbowImg from "../../../assets/rainbow.png";
import { Button } from "../../../shared/components/atoms/Button";
import { usePasswordResetRequestSubmitted } from "../hooks/usePasswordResetRequestSubmitted";


export const PasswordResetRequestSubmitted = memo(() => {
  const { handleNavigateToLogin } = usePasswordResetRequestSubmitted();

  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="flex flex-col justify-center items-center mt-[clamp(37.5px,9.1vh,154px)]">
        <h2 className="text-primary mb-[clamp(9.5px,2.3vh,83px)] text-2xl">メールをご確認ください</h2>
        <h2 className="text-primary w-[clamp(134.5px,68.7vw,536px)]">入力されているメールアドレスが登録されている場合、パスワード再設定用のメールが送信されます。
          その場合メールに記載されているリンクから再設定をおこなってください。</h2>
        <img className=" w-[clamp(115px,59.2vw,462px)] " src={rainbowImg} />
        <div>
          <Button onClick={handleNavigateToLogin} buttonColor="bg-primary" textColor="text-secondary">ログイン画面へ</Button>
        </div>
      </div>
    </div>
  )
})