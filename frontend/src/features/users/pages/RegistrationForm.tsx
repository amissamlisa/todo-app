import { memo } from "react";
import { useNavigate } from 'react-router-dom';
import { Controller, useForm } from "react-hook-form"
import { Header } from "../../../shared/components/molecules/Header";
import { Input } from "../../../shared/components/molecules/Input";
import { TwoButton } from "../../../shared/components/molecules/TwoButton";
import { PasswordInput } from "../../../shared/components/molecules/PasswordInput";


export const RegistrationForm = memo(() => {
  const navigate = useNavigate();

  type RegistrationFormType =
    {
      username: string,
      email: string,
      password: string,
      confirmPassword: string
    }
  const { control, handleSubmit, formState: { errors }, getValues} = useForm<RegistrationFormType>({
    defaultValues: {
      username: "",
      email: "",
      password: "",
      confirmPassword: ""
    }
  });
  const onPrimaryClick = (data: RegistrationFormType) => {
    console.log(data);
    navigate("/user-registration/confirm", { state: data });
  };

  const onSecondaryClick = () => {
    navigate("/");
  }
  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="bg-secondary flex flex-col items-center">
        <h2 className="text-primary mt-[clamp(15px,4vh,60px)] mb-[clamp(20px,4.8vh,80px)] text-2xl">新規会員登録</h2>
        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <Controller
            control={control}
            rules={{
              required: "ユーザー名を入力してください",
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
          {errors.username && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{errors.username.message}</p>}
        </div>
        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <Controller
            control={control}
            rules={{
              required: "メールアドレスを入力してください", pattern: {
                value: /^[a-zA-Z0-9.!#$%&'*+/\\=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
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
          {errors.email && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{errors.email.message}</p>}
        </div>

        <div className="mb-[clamp(10px,2.6vh,40px)]">
          <Controller
            control={control}
            rules={{
              required: "パスワードを入力してください",
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
          {errors.password && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{errors.password.message}</p>}
        </div>

        <div className="mb-[clamp(28px,6.6vh,112px)]">
          <Controller
            control={control}
            rules={{
              required: "確認パスワードを入力してください",
              validate: {
                validate: (value) =>
                  value === getValues("password") ||
                  "パスワードと確認パスワードが異なります",
              }
            }}
            name="confirmPassword"
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
          {errors.confirmPassword && <p className="text-red-500 w-[clamp(93px,68vw,400px)]">{errors.confirmPassword.message}</p>}
        </div>

        <div className="mb-24.5">
          <TwoButton buttonTitle1="確認画面へ" buttonTitle2="戻る" buttonBgColor="bg-primary" buttonTextColor="text-secondary" onPrimaryClick={handleSubmit(onPrimaryClick)} onSecondaryClick={onSecondaryClick} />
        </div>
      </div>
    </div>
  )
})