import { memo } from "react";
import { useNavigate } from "react-router-dom";
import { Incomplete } from "./Incomplete";

export const NotFoundPage = memo(() => {
  const navigate = useNavigate();

  const onButtonClick = () => {
    navigate("/", { replace: true });
  }

  return (
    <Incomplete
      title="ページが見つかりません"
      message={
        <>
          申し訳ございません。<br />
          お探しのページは存在しないか、移動した可能性があります。
        </>
      }
      buttonText="ログイン画面へ"
      hasLogoutButton={false}
      onButtonClick={onButtonClick}
    />
  )
}
)