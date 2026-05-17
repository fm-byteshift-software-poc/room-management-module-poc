from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exc
from typing import List
from src.models.room import Room
from src.models.room_type import RoomType
from src.schemas.room import RoomCreate, RoomUpdate
from fastapi import HTTPException

def get_all_rooms(db: Session) -> List[Room]:
    """Retrieves all rooms with their room types."""
    return db.query(Room).options(joinedload(Room.room_type)).all()

def get_room_by_id(db: Session, room_id: int) -> Room:
    """Retrieves a specific room by ID, raises 404 if not found."""
    room = db.query(Room).options(joinedload(Room.room_type)).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

def create_room(db: Session, room_data: RoomCreate) -> Room:
    """Creates a new room."""
    db_room = Room(**room_data.model_dump())
    db.add(db_room)
    try:
        db.commit()
        db.refresh(db_room)
        return db_room
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Room number already exists")

def update_room(db: Session, room_id: int, room_data: RoomUpdate) -> Room:
    """Updates an existing room."""
    room = get_room_by_id(db, room_id)
    update_data = room_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(room, key, value)
        
    try:
        db.commit()
        db.refresh(room)
        return room
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to conflict")

def delete_room(db: Session, room_id: int) -> None:
    """Deletes a room."""
    room = get_room_by_id(db, room_id)
    db.delete(room)
    db.commit()