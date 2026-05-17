from sqlalchemy.orm import Session
from typing import List
from src.models.room_type import RoomType

def get_all_room_types(db: Session) -> List[RoomType]:
    """Retrieves all room types."""
    return db.query(RoomType).all()