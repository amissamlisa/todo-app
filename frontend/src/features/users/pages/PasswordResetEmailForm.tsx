import { memo } from "react";
import { Controller, useForm } from "react-hook-form"
import { Header } from "../../../shared/components/molecules/Header";
import { Input } from "../../../shared/components/molecules/Input";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";
import { LoadingSpinner } from "../../../shared/components/atoms/LoadingSpinner";
import { usePasswordResetEmailForm } from "../hooks/usePasswordResetEmailForm";
import type { PasswordResetEmailType } from "../types/passwordResetEmail";
export const PasswordResetEmailForm = memo(() => {
  const { isLoading, handlePasswordResetEmail, handleNavigateToLogin } = usePasswordResetEmailForm();

  const { control: passwordResetEmailFormControl, handleSubmit: handlePasswordResetEmailSubmit, formState: { errors: passwordResetEmailFormErrors } } = useForm<PasswordResetEmailType>({
    defaultValues: {
      email: "",
    }
  });
  if (isLoading) {
    return <LoadingSpinner message="パスワード再設定リンク送信中..." />;
  }
  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="bg-secondary flex flex-col items-center">
        <h2 className="text-primary mt-[clamp(15px,9.1vh,60px)] mb-[clamp(20px,4.7vh,80px)] text-2xl">パスワード再設定リンク送信</h2>
        <h2 className="text-primary w-[clamp(93px,68vw,400px)] mb-[clamp(11.5px,2.7vh,46px)]">登録いただいたメールアドレスを入力してください。パスワード再設定用のメールを送信します。</h2>
        <div className="mb-[clamp(26px,6.1vh,104px)]">
          <Controller
            control={passwordResetEmailFormControl}
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
          {passwordResetEmailFormErrors.email && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{passwordResetEmailFormErrors.email.message}</p>}
        </div>
        <div className="mb-24.5">
          <TwoButton buttonTitle1="パスワード再設定リンク送信" buttonTitle2="戻る" buttonBgColor="bg-primary" buttonTextColor="text-secondary" onPrimaryClick={handlePasswordResetEmailSubmit(handlePasswordResetEmail)} onSecondaryClick={handleNavigateToLogin} />
        </div>
      </div>
    </div>
  )
})