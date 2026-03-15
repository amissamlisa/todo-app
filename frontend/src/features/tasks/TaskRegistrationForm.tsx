import { memo, useEffect, useState } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import axios from "axios";
import { Controller, useForm } from "react-hook-form"
import { Input } from "../../shared/components/molecules/Input";
import { TwoButton } from "../../shared/components/molecules/TwoButton";
import { HeaderWithLogoutIcon } from "../../shared/components/molecules/HeaderWithLogoutIcon";
import { useAuth } from "../users/auth/useAuth";
import { LoadingSpinner } from "../../shared/components/atoms/LoadingSpinner";
import dayjs from "dayjs";
import ja from "dayjs/locale/ja";

type TaskRegistrationFormType = {
  goal: string;
  currentStatus: string;
  startDate: string;
  endDate: string;
  weekdayHours: string;
  holidayHours: string;
  conditions: string;
};

dayjs.locale(ja);
export const TaskRegistrationForm = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();
  const { token } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const validateDate = (date: string, format: string) => {
    return dayjs(date, format).format(format) === date;
  }
  const { control, handleSubmit, formState: { errors }, getValues } = useForm<TaskRegistrationFormType>({
    defaultValues: {
      goal: "",
      currentStatus: "",
      startDate: "",
      endDate: "",
      weekdayHours: "",
      holidayHours: "",
      conditions: ""
    }
  });
  useEffect(() => {
    if (location.key === 'default') {
      navigate("/", { replace: true });
    }
  }, [location.key, navigate]);

  if (location.key === 'default') {
    return null;
  }
  const onPrimaryClick = async (data: TaskRegistrationFormType) => {
    try {
      setIsLoading(true);
      const toApiDate = (value: string) => value.replace(/\//g, "-");
      const payload = {
        goal: {
          goal_name: data.goal,
          status_against_goal: data.currentStatus,
          start_day: toApiDate(data.startDate),
          target_day: toApiDate(data.endDate),
          weekday_available_time: Number(data.weekdayHours),
          weekends_available_time: Number(data.holidayHours),
          task_creation_rule: data.conditions?.trim() || undefined
        },
        goal_tasks_list: []
      };

      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
      const response = await axios.post(
        `${API_BASE_URL}/goal_tasks/generate`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      console.log("APIレスポンス", response.data);
      navigate("/tasks-registration/confirm", {
        state: { form: data, generated: response.data },
        replace: true
      });
    } catch (err) {
      if (axios.isAxiosError(err)) {
        console.error(err.response?.data?.detail ?? "目標タスクの生成に失敗しました");
      } else {
        console.error("予期しないエラー", err);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const onSecondaryClick = () => {
    navigate("/top", { replace: true });
  }
  if (isLoading) {
    return <LoadingSpinner message="目標タスクを生成中..." />;
  }

  return (
    <div className="overflow-y-auto h-screen">
      <HeaderWithLogoutIcon />
      <div className="bg-secondary min-h-screen mt-[clamp(4px,0.9vh,16px)] flex flex-col items-center pb-10">
        <div className="mb-[clamp(4.5px,1vh,18px)]">
          <Controller
            control={control}
            rules={{
              required: "達成目標を入力してください",
              validate: (value) =>
                !/[ \u3000]/.test(value) || "達成目標に空白（全角・半角）は使用できません",
              maxLength: {
                value: 100,
                message: "達成目標は100文字以内で入力してください",
              },
            }}
            name="goal"
            render={({ field }) => (
              <Input
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="text"
                name={field.name}
                placeholder="例)TOEICの点数を100点上げたい"
              >
                達成目標
              </Input>
            )}
          />
        </div>
        <div className="mb-[clamp(4.5px,1vh,18px)]">
          <Controller
            control={control}
            rules={{
              required: "目標に対する現状を入力してください",
              validate: (value) =>
                !/[ \u3000]/.test(value) || "目標に対する現状に空白（全角・半角）は使用できません",
              maxLength: {
                value: 200,
                message: "目標に対する現状は200文字以内で入力してください",
              },
            }}
            name="currentStatus"
            render={({ field }) => (
              <Input
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="text"
                name={field.name}
                placeholder="例)TOEICの模擬テストで500点取得済み"
              >
                目標に対する現状
              </Input>
            )}
          />
        </div>

        <div className="mb-[clamp(4.5px,1vh,18px)]">
          <Controller
            control={control}
            rules={{
              required: "開始日を入力してください",
              validate: (value) => {
                if (/[ \u3000]/.test(value)) {
                  return "空白（全角・半角）は使用できません";
                } else if (!/^\d{4}\/\d{2}\/\d{2}$/.test(value)) {
                  return "開始日を日付形式で入力してください";
                } else if (!dayjs(value, 'YYYY/MM/DD',).isValid()) {
                  return "開始日を日付形式で入力してください";
                } else if (!validateDate(value, 'YYYY/MM/DD')) {
                  return "開始日を日付形式で入力してください";
                }
                else if (new Date(value) < new Date()) {
                  return "開始日は本日以降の日付を入力してください";
                } else if (getValues("endDate") && new Date(value) > new Date(getValues("endDate"))) {
                  return "開始日は終了日以前の日付を入力してください";
                }
              },
            }}
            name="startDate"
            render={({ field }) => (
              <Input
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="text"
                name={field.name}
                placeholder="2026/10/01"
              >
                開始日
              </Input>
            )}
          />
        </div>

        <div className="mb-[clamp(4.5px,1vh,18px)]">
          <Controller
            control={control}
            rules={{
              required: "終了日を入力してください",
              validate: (value) => {
                if (/[ \u3000]/.test(value)) {
                  return "空白（全角・半角）は使用できません";
                } else if (!/^\d{4}\/\d{2}\/\d{2}$/.test(value)) {
                  return "終了日をYYYY/MM/DDの形式で入力してください";
                } else if (!dayjs(value, 'YYYY/MM/DD', true).isValid()) {
                  return "終了日を日付形式で入力してください";
                } else if (!validateDate(value, 'YYYY/MM/DD')) {
                  return "終了日を日付形式で入力してください";
                } else if (new Date(value) < new Date()) {
                  return "終了日は本日以降の日付を入力してください";
                } else if (getValues("startDate") && new Date(value) < new Date(getValues("startDate"))) {
                  return "終了日は開始日以降の日付を入力してください";
                }
                return true;
              },
            }}
            name="endDate"
            render={({ field }) => (
              <Input
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="text"
                name={field.name}
                placeholder="2026/10/31"
              >
                終了日
              </Input>
            )}
          />
        </div>

        <div className="mb-[clamp(4.5px,1vh,18px)]">
          <Controller
            control={control}
            rules={{
              required: "平日1日の活動可能時間を入力してください",
              pattern: { value: /^[1-9]\d*$/, message: "平日1日の活動可能時間は1以上の整数で入力してください" },
              validate: (value) => {
                if (Number(value) > 720) {
                  return "平日1日の活動可能時間は1分以上720分以下で入力してください";
                }
              },
            }}
            name="weekdayHours"
            render={({ field }) => (
              <Input
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="text"
                name={field.name}
                placeholder="例)90"
              >
                平日1日の活動可能時間（分）
              </Input>
            )}
          />
        </div>

        <div className="mb-[clamp(4.5px,1vh,18px)]">
          <Controller
            control={control}
            rules={{
              required: "休日・祝日の1日の活動可能時間を入力してください",
              pattern: { value: /^[1-9]\d*$/, message: "休日・祝日の1日の活動可能時間を1以上の整数で入力してください" },
              validate: (value) => {
                if (Number(value) > 720) {
                  return "休日・祝日の1日の活動可能時間は1分以上720分以下で入力してください";
                }
              },
            }}
            name="holidayHours"
            render={({ field }) => (
              <Input
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="text"
                name={field.name}
                placeholder="例)300"
              >
                休日・祝日の1日の活動可能時間（分）
              </Input>
            )}
          />
        </div>

        <div className={Object.keys(errors).length > 0 ? "mb-[clamp(4.5px,1vh,18px)]" : "mb-[clamp(12.5px,2.8vh,50px)]"}>
          <Controller
            control={control}
            rules={{
              maxLength: {
                value: 800,
                message: "条件は800文字以内で入力してください",
              },
            }}
            name="conditions"
            render={({ field }) => (
              <Input
                value={field.value}
                onChangeText={field.onChange}
                onBlur={field.onBlur}
                textColor="text-primary"
                borderColor="border-primary"
                formType="text"
                name={field.name}
                placeholder="例)リーディングの問題を重点的に"
              >
                条件※入力は任意
              </Input>
            )}
          />
          {Object.keys(errors).length > 0 && (
            <div className="w-[clamp(93px,68vw,400px)]">
              <p className="text-red-600">
                {errors.goal?.message ||
                  errors.currentStatus?.message ||
                  errors.startDate?.message ||
                  errors.endDate?.message ||
                  errors.weekdayHours?.message ||
                  errors.holidayHours?.message ||
                  errors.conditions?.message}
              </p>
            </div>
          )}
        </div>
        <div className="pb-[clamp(21px,4.9vh,84px)]">
          <TwoButton buttonTitle1="目標タスク生成" buttonTitle2="戻る" buttonBgColor="bg-primary" buttonTextColor="text-secondary" onPrimaryClick={handleSubmit(onPrimaryClick)} onSecondaryClick={onSecondaryClick} />
        </div>
      </div>
    </div>
  )
})