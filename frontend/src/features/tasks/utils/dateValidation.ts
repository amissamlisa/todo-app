import dayjs from "dayjs";

export const isWithinThreeMonths = (startDate: string, endDate: string) => {
  const start = dayjs(startDate, "YYYY/MM/DD", true);
  const end = dayjs(endDate, "YYYY/MM/DD", true);

  if (!start.isValid() || !end.isValid()) {
    return false;
  }

  return end.diff(start, "day") <= 90;
};
