import { memo } from "react";
import { Controller, useForm } from "react-hook-form"
import { Header } from "../../../shared/components/molecules/Header";
import { PasswordInput } from "../../../shared/components/molecules/PasswordInput";
import { Button } from "../../../shared/components/atoms/Button";
import { LoadingSpinner } from "../../../shared/components/atoms/LoadingSpinner";
import { usePasswordResetForm } from "../hooks/usePasswordResetForm";
import type { PasswordResetType } from "../types/passwordReset";
export const PasswordResetForm = memo(() => {
  const { isVerifying, isValidToken, isLoading, handlePasswordReset } = usePasswordResetForm();
  const { control: passwordResetControl, handleSubmit, formState: { errors }, getValues } = useForm<PasswordResetType>({
    defaultValues: {
      password: "",
      confirmationPassword: ""
    }
  });
  if (isVerifying || !isValidToken) {
    return null;
  }
  if (isLoading) {
    return <LoadingSpinner message="パスワード再設定中..." />;
  }
  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="bg-secondary flex flex-col items-center">
        <h2 className="text-primary mt-[clamp(15px,9.1vh,60px)] mb-[clamp(20px,4.7vh,80px)] text-2xl">パスワード再設定</h2>
        <h2 className="text-center text-primary w-[clamp(93px,68vw,400px)] mb-[clamp(20px,4.7vh,80px)]">新しいパスワードを入力してください</h2>
        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <Controller
            control={passwordResetControl}
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
                新しいパスワード
              </PasswordInput>
            )}
          />
          {errors.password && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{errors.password.message}</p>}
        </div>

        <div className="mb-[clamp(28px,6.6vh,112px)]">
          <Controller
            control={passwordResetControl}
            rules={{
              required: "確認パスワードを入力してください",
              validate: (value) => {
                if (value !== getValues("password")) {
                  return "パスワードと確認パスワードが異なります";
                }
                else if (/[ \u3000]/.test(value)) {
                  return "空白（全角・半角）は使用できません";
                }
                return true;
              },
            }}
            name="confirmationPassword"
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
          {errors.confirmationPassword && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{errors.confirmationPassword.message}</p>}
          <div className="mt-[clamp(16.5px,3.9vh,66px)] ">
            <Button onClick={handleSubmit(handlePasswordReset)} buttonColor="bg-primary" textColor="text-secondary">パスワード再設定</Button>
          </div>
        </div>
      </div>
    </div>
  )
})