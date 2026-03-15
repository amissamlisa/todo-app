import { memo, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Incomplete } from "./Incomplete";

export const NotFoundPage = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.key === 'default') {
      navigate("/", { replace: true });
    }
  }, [location.key, navigate]);

  if (location.key === 'default') {
    return null;
  }

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