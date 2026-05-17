import { FC, useEffect, useState } from "react";
import { Room, RoomFormData, RoomType } from "@/types";
import { roomService, roomTypeService } from "@/services/roomService";

interface RoomFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  initialData?: Room | null;
}

const RoomFormModal: FC<RoomFormModalProps> = ({ isOpen, onClose, onSuccess, initialData }) => {
  const [formData, setFormData] = useState<RoomFormData>({
    number: "",
    floor: 0,
    capacity: 0,
    status: "available",
    room_type_id: 0,
  });

  const [roomTypes, setRoomTypes] = useState<RoomType[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isOpen) {
      setError("");
      setLoading(false);

      // Fetch room types for the dropdown
      roomTypeService.getAll().then(setRoomTypes);

      if (initialData) {
        // Edit Mode: Pre-fill form
        setFormData({
          number: initialData.number,
          floor: initialData.floor,
          capacity: initialData.capacity,
          status: initialData.status,
          room_type_id: initialData.room_type.id,
        });
      } else {
        // Create Mode: Reset form
        setFormData({
          number: "",
          floor: 0,
          capacity: 0,
          status: "available",
          room_type_id: 0,
        });
      }
    }
  }, [isOpen, initialData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (initialData?.id) {
        await roomService.update(initialData.id, formData);
      } else {
        await roomService.create(formData);
      }
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <dialog className={`modal ${isOpen ? "modal-open" : ""}`}>
      <div className="modal-box">
        <h3 className="font-bold text-lg mb-4">{initialData ? "Edit Room" : "Add Room"}</h3>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <label className="form-control w-full">
            <span className="label-text">Number</span>
            <input
              type="text"
              className="input input-bordered w-full"
              value={formData.number}
              onChange={(e) => setFormData({ ...formData, number: e.target.value })}
              required
            />
          </label>

          <div className="grid grid-cols-2 gap-4">
            <label className="form-control w-full">
              <span className="label-text">Floor</span>
              <input
                type="number"
                className="input input-bordered w-full"
                value={formData.floor}
                onChange={(e) => setFormData({ ...formData, floor: Number(e.target.value) })}
                required
              />
            </label>

            <label className="form-control w-full">
              <span className="label-text">Capacity</span>
              <input
                type="number"
                className="input input-bordered w-full"
                value={formData.capacity}
                onChange={(e) => setFormData({ ...formData, capacity: Number(e.target.value) })}
                required
              />
            </label>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <label className="form-control w-full">
              <span className="label-text">Status</span>
              <select
                className="select select-bordered w-full"
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value as any })}
              >
                <option value="available">Available</option>
                <option value="occupied">Occupied</option>
                <option value="maintenance">Maintenance</option>
                <option value="inactive">Inactive</option>
              </select>
            </label>

            <label className="form-control w-full">
              <span className="label-text">Room Type</span>
              <select
                className="select select-bordered w-full"
                value={formData.room_type_id}
                onChange={(e) => setFormData({ ...formData, room_type_id: Number(e.target.value) })}
              >
                {roomTypes.map((rt) => (
                  <option key={rt.id} value={rt.id}>
                    {rt.name}
                  </option>
                ))}
              </select>
            </label>
          </div>

          {error && <div className="alert alert-error text-sm mt-2">{error}</div>}

          <div className="flex justify-end gap-2 mt-4">
            <button type="button" className="btn" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? "Saving..." : "Save"}
            </button>
          </div>
        </form>
      </div>
      <form method="dialog" className="modal-backdrop" onClick={onClose}>
        <button>close</button>
      </form>
    </dialog>
  );
};

export default RoomFormModal;