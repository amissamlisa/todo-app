import { memo, useEffect } from "react";
import { Header } from "../../../shared/components/molecules/Header";
import { Button } from "../../../shared/components/atoms/Button";
import { useNavigate, useLocation } from 'react-router-dom';
import logoIcon from "../../../assets/cloud-icon.png"

// ログアウトのページへの遷移がうまくいかず、ログイン画面に遷移してしまう時間もかんがみていったんログアウト画面は使用しないようにする。
export const Logout = memo(() => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.key === 'default') {
      navigate("/", { replace: true });
    }
  }, [location.key, navigate]);

  const onButtonClick = () => {
    navigate("/", { replace: true });
  }

  return (
    <div className="overflow-y-auto h-screen ">
      <Header />
      <div className="flex flex-col justify-center items-center mt-[clamp(37.5px,9.1vh,154px)]">
        <h2 className="text-primary mb-[clamp(27.5px,6.5vh,0px)] text-2xl">ログアウト</h2>
        <h2 className="text-primary w-[clamp(112.5px,57.6vw,450px)]">ログアウトしました。あなたが育てた雲は、またここから成長を始めます。</h2>
        <img className=" w-[clamp(69.5px,35.6vw,278px)] " src={logoIcon} />
        <div className="mb-[clamp(251px,59.5vh,1006px)]">
          <Button onClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">ログイン画面へ</Button>
        </div>
      </div>
    </div>
  )
})