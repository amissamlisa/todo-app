import { memo, useEffect } from "react";
import { Header } from "../molecules/Header";
import notFoundImg from "../../../assets/rain-cloud.png";
import { Button } from "../atoms/Button";
import { useNavigate, useLocation } from "react-router-dom";

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
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="flex flex-col justify-center items-center mt-[clamp(37.5px,9.1vh,154px)]">
        <h2 className="text-primary mb-[clamp(27.5px,6.5vh,110px)] text-2xl">ページが見つかりません</h2>
        <h2 className="text-primary w-[clamp(112.5px,57.6vw,450px)]">申し訳ございません。お探しのページは存在しないか、移動した可能性があります</h2>
        <img className=" w-[clamp(115px,59.2vw,462px)] " src={notFoundImg} />
        <div className="mb-[clamp(251px,59.5vh,1006px)]">
          <Button onClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">ログイン画面へ</Button>
        </div>
      </div>
    </div>
  )
}
)