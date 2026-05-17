import api from "@/lib/api";
import { Room, RoomFormData, RoomType } from "@/types";

export const roomService = {
  getAll: async (): Promise<Room[]> => {
    const { data } = await api.get<Room[]>("/rooms");
    return data;
  },

  create: async (payload: RoomFormData): Promise<Room> => {
    const { data } = await api.post<Room>("/rooms", payload);
    return data;
  },

  update: async (id: number, payload: Partial<RoomFormData>): Promise<Room> => {
    const { data: response } = await api.patch<Room>(`/rooms/${id}`, payload);
    return response;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/rooms/${id}`);
  },
};

export const roomTypeService = {
  getAll: async (): Promise<RoomType[]> => {
    const { data } = await api.get<RoomType[]>("/room-types");
    return data;
  },
};
