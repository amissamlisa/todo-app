import { memo } from "react";

type LoadingSpinnerProps = {
  message?: string;
};

export const LoadingSpinner = memo(({ message = "読み込み中..." }: LoadingSpinnerProps) => {
  return (
    <div className="overflow-y-auto h-screen flex items-center justify-center bg-secondary">
      <div className="flex flex-col items-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary"></div>
        <p className="mt-4 text-primary text-xl">{message}</p>
      </div>
    </div>
  );
});
