import { memo } from "react";
import { Controller, useForm } from "react-hook-form"
import { Link, useNavigate } from 'react-router-dom';
import { Logo } from "../../../shared/components/atoms/Logo";
import { Input } from "../../../shared/components/molecules/Input";
import { PasswordInput } from "../../../shared/components/molecules/PasswordInput";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";
import { type LoginFormType } from "../types/loginForm";
import { useAuth } from "../auth/useAuth";

export const Login = memo(() => {
  const navigate = useNavigate();
  const { control, handleSubmit, formState: { errors } } = useForm<LoginFormType>({
    defaultValues: {
      email: "",
      password: "",
    }
  });
  const { login, loginErrorMessageFromServer, clearLoginErrorMessage } = useAuth();
  const onPrimaryClick = async (data: LoginFormType) => {
    console.log(data);
    const isSucceeded = await login(data.email, data.password);
    console.log(isSucceeded);
    if (isSucceeded) {
      navigate("/top", { replace: true });
       clearLoginErrorMessage();
    } 
  };

  const onSecondaryClick = () => {
    navigate("/user-registration", { replace: true });
    if (loginErrorMessageFromServer !== null) {
        clearLoginErrorMessage();
    }
  }
  return (
    <div className="bg-primary h-screen flex flex-col items-center overflow-y-auto">
      <div className="mt-[clamp(60px,13.1vh,200px)]">
        <Logo fontSize="text-4xl" imageSize="w-[139px] h-[139px]" />
      </div>
      <div className="mt-[clamp(50px,5.3vh,100px)]">
        <Controller
          control={control}
          rules={{
            required: "メールアドレスを入力してください",
          }}
          name="email"
          render={({ field }) => (
            <Input
              value={field.value}
              onChangeText={field.onChange}
              onBlur={field.onBlur}
              textColor="text-secondary"
              borderColor="border-secondary"
              formType="text"
              name={field.name}
            >
              メールアドレス
            </Input>
          )}
        />
      </div>
      <div className="mt-[clamp(9px,1.6vh,30px)]">
        <Controller
          control={control}
          rules={{
            required: "パスワードを入力してください",
          }}
          name="password"
          render={({ field }) => (
            <PasswordInput
              value={field.value}
              onChangeText={field.onChange}
              onBlur={field.onBlur}
              textColor="text-secondary"
              borderColor="border-secondary"
              formType="password"
              name={field.name}
            >
              パスワード
            </PasswordInput>
          )}
        />
      </div>
      <div className="text-right w-[clamp(93px,68vw,400px)]">
        <Link className="text-secondary" to="/password-reset-email-form">パスワードを忘れた方はこちら</Link>
      </div>

        <p className="text-red-500">{errors.email?.message || errors.password?.message }</p>

      {loginErrorMessageFromServer && (
        <p className="text-red-500">{loginErrorMessageFromServer}</p>
      )}
      <div className="mt-[clamp(9px,2.1vh,32px)]">
        <TwoButton buttonTitle1="ログイン" buttonTitle2="新規登録" buttonBgColor="bg-secondary" buttonTextColor="text-primary" onPrimaryClick={handleSubmit(onPrimaryClick)} onSecondaryClick={onSecondaryClick} ></TwoButton>
      </div>
    </div>
  )
})