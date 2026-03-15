import { memo } from "react";
import { HeaderWithLogoutIcon } from "../molecules/HeaderWithLogoutIcon";
import rainCloudImg from "../../../assets/rain-cloud.png";
import { Button } from "../atoms/Button";

type IncompleteProps = {
  title: string;
  message: string;
  buttonText: string;
  onButtonClick: () => void;
};

export const Incomplete = memo(
  ({ title, message, buttonText, onButtonClick }: IncompleteProps) => {
    return (
      <div className="overflow-y-auto h-screen ">
        <HeaderWithLogoutIcon />
        <div className="flex flex-col justify-center items-center">
          <h2 className="text-primary mt-[clamp(15px,9.1vh,60px)] mb-[clamp(20px,4.7vh,80px)] text-2xl">
            {title}
          </h2>
          <h2 className="text-primary">{message}</h2>
          <img className="w-[clamp(115px,59.2vw,462px)]" src={rainCloudImg} />
          <div className="mb-[clamp(251px,59.5vh,1006px)]">
            <Button onClick={onButtonClick} buttonColor="bg-primary" textColor="text-secondary">
              {buttonText}
            </Button>
          </div>
        </div>
      </div>
    );
  }
);
