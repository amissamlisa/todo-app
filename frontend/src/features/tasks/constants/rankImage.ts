import CloudIcon from "../../../assets/cloud.png";
import DropletIcon from "../../../assets/droplet.png";
import GlowingCloudIcon from "../../../assets/glowing-cloud.png";
import MistIcon from "../../../assets/mist.png";
import type { Rank } from "../types/rank";

export const rankImageMap: Record<Rank, string> = {
    "雫": DropletIcon,
    "霧": MistIcon,
    "雲": CloudIcon,
    "光雲": GlowingCloudIcon,
  };