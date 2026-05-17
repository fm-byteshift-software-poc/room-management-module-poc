from sqlalchemy import Column, Integer, String, Date, ForeignKey
from src.config.database import Base

# Reservation logic is not implemented. This table exists so Room.current_reservation_id has a valid foreign key target when booking endpoints are added in a future phase.
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guest_name = Column(String(150), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)