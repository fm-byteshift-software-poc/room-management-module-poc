import { FC } from 'react';

interface PageHeaderProps {
  onAdd: () => void;
}

const PageHeader: FC<PageHeaderProps> = ({ onAdd }) => {
  return (
    <div className="flex justify-between items-center mb-6">
      <h1 className="text-3xl font-bold">Room Management</h1>
      <button className="btn btn-primary" onClick={onAdd}>Add Room</button>
    </div>
  );
};

export default PageHeader;