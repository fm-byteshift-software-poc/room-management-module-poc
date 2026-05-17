import enum
from sqlalchemy import Column, Integer, String, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class RoomStatus(str, enum.Enum):
    available = "available"
    occupied = "occupied"
    maintenance = "maintenance"
    inactive = "inactive"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(10), nullable=False, unique=True)
    floor = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(SAEnum(RoomStatus), nullable=False, default=RoomStatus.available)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    
    # Nullable foreign key to reservations table - structural anchor for future booking workflows
    current_reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=True)

    # Relationships
    room_type = relationship("RoomType", back_populates="rooms", lazy="joined")