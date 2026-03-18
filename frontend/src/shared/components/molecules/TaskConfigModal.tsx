import { memo, useEffect } from "react";
import { Controller, useForm } from "react-hook-form";
import { ModalButton } from "../atoms/ModalButton";
import logoIcon from "../../../assets/cloud_icon.png"
import { Input } from "./Input";
import type { TaskConfigModalFormType } from "../../types/taskConfigModalForm";
import type { TaskConfigModalProps } from "../../types/taskConfigModal";

export const TaskConfigModal = memo(({
  showFlag,
  taskName,
  estimatedTime,
  deadline,
  errorMessage,
  title = "タスク設定",
  hasTwoButtons = true,
  setIsOpenModal,
  onChangeTaskName,
  onChangeEstimatedTime,
  onChangeDeadline,
  onClickChange,
}: TaskConfigModalProps) => {
  const validateDate = (date: string, format: string) => {
    const normalizedDate = date.replace(/\//g, "-");
    const [year, month, day] = normalizedDate.split("-").map(Number);
    if (!year || !month || !day) return false;

    const parsedDate = new Date(year, month - 1, day);
    return (
      parsedDate.getFullYear() === year &&
      parsedDate.getMonth() === month - 1 &&
      parsedDate.getDate() === day &&
      format === "YYYY/MM/DD"
    );
  };

  const { control, handleSubmit, reset, formState: { errors } } = useForm<TaskConfigModalFormType>({
    defaultValues: {
      taskName,
      estimatedTime,
      deadline,
    },
  });

  useEffect(() => {
    reset({
      taskName,
      estimatedTime,
      deadline,
    });
  }, [taskName, estimatedTime, deadline, showFlag, reset]);

  const closeModal = () => {
    setIsOpenModal(false);
  };

  const displayErrorMessage =
    errors.taskName?.message ||
    errors.estimatedTime?.message ||
    errors.deadline?.message ||
    errorMessage;

  return (
    <>
      {showFlag ? (
        <div className="fixed top-0 left-0 w-full h-full bg-black/70 bg-opacity-50 flex items-center justify-center z-50">
          <div className="flex flex-col items-center justify-between w-[clamp(156.5px,80vw,626px)] bg-white rounded-[3px]">
            <div className="text-center w-full">
              <div className="bg-primary flex justify-center items-center relative">
                <img className="w-[clamp(21px,10.7vw,50px)] absolute left-0" src={logoIcon} alt="Logo" />
                <p className="text-lg text-secondary">{title}</p>
              </div>
            </div>
            <div className="w-full flex flex-col items-center gap-[clamp(4.5px,1vh,18px)] px-3 py-3">
              <Controller
                control={control}
                name="taskName"
                rules={{
                  required: "タスク名を入力してください",
                  maxLength: {
                    value: 100,
                    message: "タスク名は100文字以内で入力してください",
                  },
                }}
                render={({ field }) => (
                  <Input
                    value={field.value}
                    onChangeText={(value) => {
                      field.onChange(value);
                      onChangeTaskName(value);
                    }}
                    onBlur={field.onBlur}
                    textColor="text-primary"
                    borderColor="border-primary"
                    formType="text"
                    name={field.name}
                    placeholder="例)英単語を30個覚える"
                  >
                    タスク名
                  </Input>
                )}
              />
              <Controller
                control={control}
                name="estimatedTime"
                rules={{
                  required: "推定時間を入力してください",
                  pattern: {
                    value: /^[1-9]\d*$/,
                    message: "推定時間は1以上の整数で入力してください",
                  },
                  validate: (value) => {
                    if (Number(value) > 720) {
                      return "推定時間は720分以下で入力してください";
                    }
                    return true;
                  },
                }}
                render={({ field }) => (
                  <Input
                    value={field.value}
                    onChangeText={(value) => {
                      field.onChange(value);
                      onChangeEstimatedTime(value);
                    }}
                    onBlur={field.onBlur}
                    textColor="text-primary"
                    borderColor="border-primary"
                    formType="text"
                    name={field.name}
                    placeholder="例)30"
                  >
                    タスクにかかる推定時間（分）
                  </Input>
                )}
              />
              <Controller
                control={control}
                name="deadline"
                rules={{
                  required: "期限を入力してください",
                  validate: (value) => {
                    if (!/^\d{4}\/\d{2}\/\d{2}$/.test(value)) {
                      return "期限をYYYY/MM/DD形式で入力してください";
                    }

                    if (!validateDate(value, "YYYY/MM/DD")) {
                      return "期限を正しい日付で入力してください";
                    }

                    const parsedDate = new Date(value.replace(/\//g, "-"));
                    const today = new Date();
                    today.setHours(0, 0, 0, 0);
                    if (parsedDate <= today) {
                      return "期限は明日以降の日付を入力してください";
                    }

                    return true;
                  },
                }}
                render={({ field }) => (
                  <Input
                    value={field.value}
                    onChangeText={(value) => {
                      field.onChange(value);
                      onChangeDeadline(value);
                    }}
                    onBlur={field.onBlur}
                    textColor="text-primary"
                    borderColor="border-primary"
                    formType="text"
                    name={field.name}
                    placeholder="2026/10/31"
                  >
                    タスクの期限
                  </Input>
                )}
              />
              {displayErrorMessage ? (
                <div className="w-[clamp(93px,68vw,400px)]">
                  <p className="text-red-600">{displayErrorMessage}</p>
                </div>
              ) : null}
            </div>
            {hasTwoButtons ? (
              <div className="pb-[clamp(8px,1.8vh,32px)] flex justify-around ">
                <ModalButton onClick={closeModal} buttonColor="bg-primary" textColor="text-secondary">キャンセル</ModalButton>
                <div className="mr-[clamp(35px,17.9vw,140px)]"></div>
                <ModalButton onClick={handleSubmit(() => onClickChange?.())} buttonColor="bg-primary" textColor="text-secondary">登録</ModalButton>
              </div>) : (
              <div className="pb-[clamp(8px,1.8vh,32px)]">
                <ModalButton onClick={closeModal} buttonColor="bg-primary" textColor="text-secondary">閉じる</ModalButton>
              </div>
            )}
          </div>
        </div>
      ) : (
        <></>
      )}
    </>
  );
});