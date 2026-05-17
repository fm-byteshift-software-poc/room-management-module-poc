export interface RoomType {
  id: number;
  name: string;
  description: string | null;
}

export interface Room {
  id: number;
  number: string;
  floor: number;
  capacity: number;
  status: "available" | "occupied" | "maintenance" | "inactive";
  current_reservation_id: number | null;
  room_type: RoomType;
}

export interface RoomFormData {
  number: string;
  floor: number;
  capacity: number;
  status: Room["status"];
  room_type_id: number;
}
