import { memo } from "react";
import { Controller, useForm } from "react-hook-form"
import { Link } from 'react-router-dom';
import { Logo } from "../../../shared/components/atoms/Logo";
import { Input } from "../../../shared/components/molecules/Input";
import { PasswordInput } from "../../../shared/components/molecules/PasswordInput";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";
import { type LoginFormType } from "../types/loginForm";
import { useLoginPage } from "../hooks/useLoginPage";

export const Login = memo(() => {
  const {
    loginErrorMessageFromServer,
    handleLogin,
    handleNavigateToRegistration,
  } = useLoginPage();
  const { control: loginFormControl, handleSubmit: handleLoginSubmit, formState: { errors: loginFormErrors } } = useForm<LoginFormType>({
    defaultValues: {
      email: "",
      password: "",
    }
  });
  return (
    <div className="bg-primary h-screen flex flex-col items-center overflow-y-auto">
      <div className="mt-[clamp(60px,13.1vh,200px)]">
        <Logo fontSize="text-4xl" imageSize="w-[139px] h-[139px]" />
      </div>
      <div className="mt-[clamp(50px,5.3vh,100px)]">
        <Controller
          control={loginFormControl}
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
          control={loginFormControl}
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
      <p className="text-red-500">{loginFormErrors.email?.message || loginFormErrors.password?.message}</p>
      {loginErrorMessageFromServer && (
        <p className="text-red-500">{loginErrorMessageFromServer}</p>
      )}
      <div className="mt-[clamp(9px,2.1vh,32px)]">
        <TwoButton buttonTitle1="ログイン" buttonTitle2="新規登録" buttonBgColor="bg-secondary" buttonTextColor="text-primary" onPrimaryClick={handleLoginSubmit(handleLogin)} onSecondaryClick={handleNavigateToRegistration} ></TwoButton>
      </div>
    </div>
  )
})