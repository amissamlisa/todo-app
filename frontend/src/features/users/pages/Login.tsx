import { memo } from "react";
import { Link } from 'react-router-dom';
import { Logo } from "../../../shared/components/atoms/Logo";
import { Input } from "../../../shared/components/molecules/Input";
import { PasswordInput } from "../../../shared/components/molecules/PasswordInput";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";

export const Login = memo(() => {
  return (
    <div className="bg-primary h-screen flex flex-col items-center overflow-y-auto">
      <div className="mt-[clamp(60px,13.1vh,200px)]">
        <Logo fontSize="text-4xl" imageSize="139px" />
      </div>
      <div className="mt-[clamp(50px,5.3vh,100px)]">
        <Input textColor="text-secondary" borderColor="border-secondary" formType="text" formName="email">メールアドレス</Input>
      </div>
      <div className="mt-[clamp(9px,1.6vh,30px)]">
        <PasswordInput textColor="text-secondary" borderColor="border-secondary" formName="password">パスワード</PasswordInput>
      </div>
      <div className="text-right w-[clamp(93px,68vw,400px)]"><Link className="text-secondary" to="/forgot-password">パスワードを忘れた方はこちら</Link></div>
      <div className="mt-[clamp(30px,6.6vh,70px)] mb-[clamp(60px,13.1vh,200px)]">
        <TwoButton buttonTitle1="ログイン" buttonTitle2="新規登録"></TwoButton>
      </div>
    </div>
  )
})