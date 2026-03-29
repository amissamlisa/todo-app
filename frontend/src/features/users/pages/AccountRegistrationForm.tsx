import { memo } from "react";
import { Controller, useForm } from "react-hook-form"
import { Header } from "../../../shared/components/molecules/Header";
import { Input } from "../../../shared/components/molecules/Input";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";
import { PasswordInput } from "../../../shared/components/molecules/PasswordInput";
import { type RegistrationFormType } from "../types/registrationForm";
import { useAccountRegistrationForm } from "../hooks/useAccountRegistrationForm";

export const AccountRegistrationForm = memo(() => {
  const { handleAccountRegistrationSubmit, handleNavigateToTop } = useAccountRegistrationForm();
  const { control: registrationFormControl, handleSubmit: handleRegistrationFormSubmit, formState: { errors: registrationErrors }, getValues: getRegistrationValues } = useForm<RegistrationFormType>({
    defaultValues: {
      username: "",
      email: "",
      password: "",
      confirmation_password: ""
    }
  });
  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="bg-secondary flex flex-col items-center">
        <h2 className="text-primary mt-[clamp(15px,4vh,60px)] mb-[clamp(20px,4.8vh,80px)] text-2xl">新規会員登録</h2>
        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <Controller
            control={registrationFormControl}
            rules={{
              required: "ユーザー名を入力してください",
              validate: (value) =>
                !/[ \u3000]/.test(value) || "空白（全角・半角）は使用できません",
            }}
            name="username"
            render={({ field }) => (
              <Input
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="text"
                name={field.name}
              >
                ユーザー名
              </Input>
            )}
          />
          {registrationErrors.username && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{registrationErrors.username.message}</p>}
        </div>
        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <Controller
            control={registrationFormControl}
            rules={{
              required: "メールアドレスを入力してください",
              validate: (value) =>
                !/[ \u3000]/.test(value) || "空白（全角・半角）は使用できません",
              pattern: {
                value: /^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/,
                message: "メールアドレスはメールアドレス形式で入力してください",
              },
            }}
            name="email"
            render={({ field }) => (
              <Input
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="text"
                name={field.name}
              >
                メールアドレス
              </Input>
            )}
          />
          {registrationErrors.email && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{registrationErrors.email.message}</p>}
        </div>

        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <Controller
            control={registrationFormControl}
            rules={{
              required: "パスワードを入力してください",
              validate: (value) =>
                !/[ \u3000]/.test(value) || "空白（全角・半角）は使用できません"
              ,
              minLength: {
                value: 10,
                message: "パスワードは10桁以上で入力してください",
              },
              pattern: {
                value: /^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])[A-Za-z0-9\W_]+$/,
                message: "パスワードは英大文字・小文字・数字・記号を各1文字以上使用してください",
              }
            }}
            name="password"
            render={({ field }) => (
              <PasswordInput
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="password"
                name={field.name}
              >
                パスワード
              </PasswordInput>
            )}
          />
          {registrationErrors.password && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{registrationErrors.password.message}</p>}
        </div>

        <div className="mb-[clamp(28px,6.6vh,112px)]">
          <Controller
            control={registrationFormControl}
            rules={{
              required: "確認パスワードを入力してください",
              validate: (value) => {
                if (value !== getRegistrationValues("password")) {
                  return "パスワードと確認パスワードが異なります";
                }
                else if (/[ \u3000]/.test(value)) {
                  return "空白（全角・半角）は使用できません";
                }
              },
            }}
            name="confirmation_password"
            render={({ field }) => (
              <PasswordInput
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="password"
                name={field.name}
              >
                確認パスワード
              </PasswordInput>
            )}
          />
          {registrationErrors.confirmation_password && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{registrationErrors.confirmation_password.message}</p>}
        </div>

        <div className="mb-24.5">
          <TwoButton buttonTitle1="確認画面へ" buttonTitle2="戻る" buttonBgColor="bg-primary" buttonTextColor="text-secondary" onPrimaryClick={handleRegistrationFormSubmit(handleAccountRegistrationSubmit)} onSecondaryClick={handleNavigateToTop} />
        </div>
      </div>
    </div>
  )
})