import { memo } from "react";
import { HeaderWithLogoutIcon } from "../molecules/HeaderWithLogoutIcon";
import rainCloudImg from "../../../assets/rain-cloud.png";
import { Button } from "../atoms/Button";
import { Header } from "../molecules/Header";
import type { IncompleteProps } from "../../types/incomplete";

export const Incomplete = memo(
  ({ title, message, buttonText, hasLogoutButton, onClick, hasButton = true }: IncompleteProps) => {
    return (
      <div className="overflow-y-auto h-screen ">
        {hasLogoutButton ?
          (<HeaderWithLogoutIcon />) :
          (<Header />)
        }
        <div className="flex flex-col justify-center items-center">
          <h2 className="text-primary mt-[clamp(15px,9.1vh,60px)] mb-[clamp(20px,4.7vh,80px)] text-2xl">
            {title}
          </h2>
          <h2 className="text-primary text-center">{message}</h2>
          <img className="w-[clamp(115px,59.2vw,462px)]" src={rainCloudImg} />
          {hasButton ? (
            <div>
              <Button onClick={onClick ?? (() => undefined)} buttonColor="bg-primary" textColor="text-secondary">
                {buttonText}
              </Button>
            </div>
          ) : null}
        </div>
      </div>
    );
  }
);
