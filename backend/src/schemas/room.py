from pydantic import BaseModel, Field
from typing import Optional

# Nested schema for RoomType
class RoomTypeSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]

# Output schema (API response)
class RoomRead(BaseModel):
    id: int
    number: str
    floor: int
    capacity: int
    status: str
    current_reservation_id: Optional[int] = None  # Always present in response, null for seed data
    room_type: RoomTypeSchema

# Input schema (Create request)
class RoomCreate(BaseModel):
    number: str
    floor: int
    capacity: int
    status: str
    room_type_id: int

# Input schema (Update request - all fields optional)
class RoomUpdate(BaseModel):
    number: Optional[str] = None
    floor: Optional[int] = None
    capacity: Optional[int] = None
    status: Optional[str] = None
    room_type_id: Optional[int] = None