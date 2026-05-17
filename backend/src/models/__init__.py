# src/models/__init__.py

# Import Base to ensure all models share the same metadata registry
from src.config.database import Base

# Import model classes explicitly to register them in Base.metadata
from .room_type import RoomType
from .reservation import Reservation
from .room import Room, RoomStatus

# Expose classes for external imports (optional but clean)
__all__ = ["RoomType", "Reservation", "Room", "RoomStatus", "Base"]