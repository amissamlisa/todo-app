import { memo, useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import { Logo } from "../../../shared/components/atoms/Logo";
import { Input } from "../../../shared/components/molecules/Input";
import { PasswordInput } from "../../../shared/components/molecules/PasswordInput";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";

export const Login = memo(() => {
  const navigate = useNavigate();
  const [formValues, setFormValues] = useState({
    email: "",
    password: "",
  });
  const handleValueChange =
    (formName: string, newValue: string) => {
      console.log(formValues);
      setFormValues((prev) => ({
        ...prev,
        [formName]: newValue,
      }));
    };

  const onPrimaryClick = () => {
    navigate("/");
  }

  const onSecondaryClick = () => {
    navigate("/user-registration");
  }
  return (
    <div className="bg-primary h-screen flex flex-col items-center overflow-y-auto">
      <div className="mt-[clamp(60px,13.1vh,200px)]">
        <Logo fontSize="text-4xl" imageSize="w-[139px] h-[139px]" />
      </div>
      <div className="mt-[clamp(50px,5.3vh,100px)]">
        <Input handleValueChange={handleValueChange} textColor="text-secondary" borderColor="border-secondary" formType="text" formName="email">メールアドレス</Input>
      </div>
      <div className="mt-[clamp(9px,1.6vh,30px)]">
        <PasswordInput handleValueChange={handleValueChange} textColor="text-secondary" borderColor="border-secondary" formName="password">パスワード</PasswordInput>
      </div>
      <div className="text-right w-[clamp(93px,68vw,400px)]"><Link className="text-secondary" to="/forgot-password">パスワードを忘れた方はこちら</Link></div>
      <div className="mt-[clamp(30px,6.6vh,70px)] mb-[clamp(60px,13.1vh,200px)]">
        <TwoButton buttonTitle1="ログイン" buttonTitle2="新規登録" buttonBgColor="bg-secondary" buttonTextColor="text-primary" onPrimaryClick={onPrimaryClick} onSecondaryClick={onSecondaryClick} ></TwoButton>
      </div>
    </div>
  )
})