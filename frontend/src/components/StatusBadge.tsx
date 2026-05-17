import { FC } from 'react';

interface StatusBadgeProps {
  status: string;
}

const StatusBadge: FC<StatusBadgeProps> = ({ status }) => {
  const colorMap: Record<string, string> = {
    available: 'badge-success',
    occupied: 'badge-error',
    maintenance: 'badge-warning',
    inactive: 'badge-neutral',
  };

  return (
    <span className={`badge ${colorMap[status] || 'badge-ghost'} gap-1`}>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
};

export default StatusBadge;