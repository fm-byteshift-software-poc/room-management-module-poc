import { useEffect, useState } from "react";
import { Room } from "@/types";
import { roomService } from "@/services/roomService";
import PageHeader from "@/components/PageHeader";
import RoomTable from "@/components/RoomTable";
import RoomFormModal from "@/components/RoomFormModal";

function App() {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editRoom, setEditRoom] = useState<Room | null>(null);

  useEffect(() => {
    roomService.getAll().then(setRooms).catch(console.error);
  }, []);

  const handleAdd = () => {
    setEditRoom(null);
    setIsModalOpen(true);
  };

  const handleEdit = (room: Room) => {
    setEditRoom(room);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    await roomService.delete(id);
    roomService.getAll().then(setRooms);
  };

  const handleSuccess = () => {
    roomService.getAll().then(setRooms);
  };

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <PageHeader onAdd={handleAdd} />
      <RoomTable rooms={rooms} onEdit={handleEdit} onDelete={handleDelete} />
      <RoomFormModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={handleSuccess}
        initialData={editRoom}
      />
    </div>
  );
}

export default App;