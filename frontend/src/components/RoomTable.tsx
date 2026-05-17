import { FC } from 'react';
import { Room } from '@/types';
import StatusBadge from '@/components/StatusBadge';

interface RoomTableProps {
  rooms: Room[];
  onEdit: (room: Room) => void;
  onDelete: (id: number) => void;
}

const RoomTable: FC<RoomTableProps> = ({ rooms, onEdit, onDelete }) => {
  return (
    <div className="overflow-x-auto rounded-box border border-base-200">
      <table className="table w-full">
        <thead className="bg-base-200">
          <tr>
            <th>Number</th>
            <th>Floor</th>
            <th>Type</th>
            <th>Capacity</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rooms.map((room) => (
            <tr key={room.id} className="hover">
              <td>{room.number}</td>
              <td>{room.floor}</td>
              <td>{room.room_type?.name}</td>
              <td>{room.capacity}</td>
              <td><StatusBadge status={room.status} /></td>
              <td className="space-x-2">
                <button className="btn btn-sm" onClick={() => onEdit(room)}>Edit</button>
                <button className="btn btn-sm btn-error btn-outline" onClick={() => onDelete(room.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RoomTable;