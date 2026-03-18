import { ImCross } from "react-icons/im";
import type { ListProps } from "../../types/list";

export const List = ({
  mainTitle,
  showList,
  images,
  explanations,
  titles,
  setShowList,
}: ListProps) => {

  if (!showList) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/70 flex items-start justify-start">
      <div className="relative z-60 h-[clamp(297.5px,70.4vh,1190px)] w-[clamp(147.5px,75.4vw,590px)] bg-secondary rounded-r-lg shadow-lg pt-[clamp(25px,5.9vh,100px)]  pb-[clamp(25px,5.9vh,100px)]">
        <h2 className=" text-primary text-center text-lg font-bold mb-4">{mainTitle}</h2>
        <ImCross
          className="absolute top-10 right-5 cursor-pointer text-primary"
          onClick={() => setShowList(false)}
        />
        <div className="flex flex-col gap-[clamp(10px,2.4vh,40px)] overflow-y-auto h-full pr-2">
          {titles.map((title, index) => (
            <div key={`${title}-${index}`} className="flex items-center gap-2">
              <div className="flex flex-col items-center">
                <div className="relative w-20 h-20 flex items-center justify-center">
                  <img
                    src={images[index]}
                    alt={title}
                    className="w-16 h-16 object-contain relative z-10"
                  />
                  <span className="absolute w-20 h-20 border-2 border-primary rounded-full z-0" />
                </div>
                <h2 className="text-primary">{title}</h2>
              </div>
              <div className="text-primary flex flex-col items-start px-2">
                {explanations[index]
                  ?.split("\n")
                  .map((line, lineIndex) => (
                    <p key={`${title}-${lineIndex}`}>{line}</p>
                  ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};