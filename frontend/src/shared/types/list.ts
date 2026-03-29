export type ListProps = {
  mainTitle: string;
  images: string[];
  explanations: string[];
  titles: string[];
  showList: boolean;
  setShowList: (show: boolean) => void;
};