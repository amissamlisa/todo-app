import dayjs from "dayjs";

export const isWithinOneWeek = (startDate: string, endDate: string) => {
  const start = dayjs(startDate, "YYYY/MM/DD", true);
  const end = dayjs(endDate, "YYYY/MM/DD", true);

  if (!start.isValid() || !end.isValid()) {
    return false;
  }

  const diffDays = end.diff(start, "day");
  return diffDays >= 0 && diffDays <= 7;
};
