import { memo, useState } from "react";
import { useNavigate } from 'react-router-dom';
import { Header } from "../../../shared/components/molecules/Header";
import { Input } from "../../../shared/components/molecules/Input";
import { PasswordInput } from "../../../shared/components/molecules/PasswordInput";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";


export const RegistrationForm = memo(() => {
  const navigate = useNavigate();
  const [formValues, setFormValues] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: ""
  });
  const handleValueChange =
    (formName: string, newValue: string) => {
      setFormValues((prev) => ({
        ...prev,
        [formName]: newValue,
      }));
      console.log(formValues);
    };
  const onPrimaryClick = () => {
    navigate("/user-registration/confirm", {state: formValues});
  }

  const onSecondaryClick = () => {
    navigate("/");
  }
  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="bg-secondary flex flex-col items-center">
        <h2 className="text-primary mt-[clamp(15px,4vh,60px)] mb-[clamp(20px,4.8vh,80px)] text-2xl">新規会員登録</h2>
        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <Input handleValueChange={handleValueChange} textColor="text-primary" borderColor="border-primary" formType="text" formName="username">ユーザー名</Input>
        </div>
        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <Input handleValueChange={handleValueChange} textColor="text-primary" borderColor="border-primary" formType="text" formName="email">メールアドレス</Input>
        </div>
        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <PasswordInput handleValueChange={handleValueChange} textColor="text-primary" borderColor="border-primary" formName="password">パスワード</PasswordInput>
        </div>
        <div className="mb-[clamp(28px,6.6vh,112px)]">
          <PasswordInput handleValueChange={handleValueChange} textColor="text-primary" borderColor="border-primary" formName="confirmPassword">確認パスワード</PasswordInput>
        </div>
        <div className="mb-24.5">
          <TwoButton buttonTitle1="確認画面へ" buttonTitle2="戻る" buttonBgColor="bg-primary" buttonTextColor="text-secondary" onPrimaryClick={onPrimaryClick} onSecondaryClick={onSecondaryClick} />
        </div>
      </div>
    </div>
  )
})