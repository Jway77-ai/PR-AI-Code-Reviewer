import React from 'react';
import { format, formatDistanceToNow, isToday, isWithinInterval, subDays } from 'date-fns';

interface DateInfoProps {
  createdDate: string | Date;
  lastModified: string | Date;
}

const DateInfo: React.FC<DateInfoProps> = ({ createdDate, lastModified }) => {
  const created = new Date(createdDate);
  const modified = new Date(lastModified);

  // Helper function to format the date/time difference
  const formatDate = (date: Date) => {
    if (isToday(date)) {
      // Display "X hours ago" if it's today
      return formatDistanceToNow(date, { addSuffix: true });
    } else if (isWithinInterval(date, { start: subDays(new Date(), 6), end: new Date() })) {
      // Display "X days ago" if within the last 7 days
      return formatDistanceToNow(date, { addSuffix: true });
    } else {
      // Display full date if longer than 7 days ago
      return format(date, 'yyyy-MM-dd');
    }
  };

  return (
    <div>
      <p className="text-gray-600 text-sm ml-3">
        • Created {formatDate(created)} • Last updated {formatDate(modified)}
      </p>
    </div>
  );
};

export default DateInfo;
