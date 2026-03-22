import { memo } from "react";
import partyPopper from "../../../assets/party-popper.png";
import { ModalButton } from "../atoms/ModalButton";
import logoIcon from "../../../assets/cloud_icon.png"
import type { TwoButtonModalProps } from "../../types/twoButtonModal";

export const TwoButtonModal = memo(({ title, content, hasPartyPopper, hasTwoButtons, showFlag, setIsOpenModal, onClickChange }: TwoButtonModalProps) => {
  const closeModal = () => {
    setIsOpenModal(false);
  }

  return (
    <>
      {showFlag ? (
        <div className="fixed top-0 left-0 w-full h-full bg-black/70 bg-opacity-50 flex items-center justify-center z-20">
          <div className="flex flex-col items-center justify-between w-[clamp(156.5px,80vw,626px)] h-[clamp(97.5px,19.5vh,330px)] bg-white  rounded-[3px]">
            <div className="text-center w-full">
              <div className="bg-primary flex justify-center items-center relative">
                <img className="w-[clamp(21px,10.7vw,50px)] absolute left-0" src={logoIcon} alt="Logo" />
                <p className="text-lg text-secondary">{title}</p>
                {hasPartyPopper && <div><img className="w-[clamp(13px,6.6vw,52px)]" src={partyPopper} alt="Party Popper" /></div>}
              </div>

            </div>
            <p className="text-primary" >{content}</p>
            {hasTwoButtons ? (
              <div className="pb-[clamp(8px,1.8vh,32px)] flex justify-around ">
                <ModalButton onClick={closeModal} buttonColor="bg-primary" textColor="text-secondary">いいえ</ModalButton>
                <div className="mr-[clamp(35px,17.9vw,140px)]"></div>
                <ModalButton onClick={onClickChange} buttonColor="bg-primary" textColor="text-secondary">はい</ModalButton>
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
  )
})