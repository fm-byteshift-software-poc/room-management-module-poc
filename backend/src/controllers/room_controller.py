from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.config.database import get_db
from src.schemas.room import RoomCreate, RoomUpdate, RoomRead
from src.services import room_service

router = APIRouter()

@router.get("/", response_model=List[RoomRead])
def list_rooms(db: Session = Depends(get_db)):
    return room_service.get_all_rooms(db)

@router.post("/", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
def create_room(room_in: RoomCreate, db: Session = Depends(get_db)):
    return room_service.create_room(db, room_in)

@router.get("/{room_id}", response_model=RoomRead)
def get_room(room_id: int, db: Session = Depends(get_db)):
    return room_service.get_room_by_id(db, room_id)

@router.patch("/{room_id}", response_model=RoomRead)
def update_room(room_id: int, room_in: RoomUpdate, db: Session = Depends(get_db)):
    return room_service.update_room(db, room_id, room_in)

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room_service.delete_room(db, room_id)
    return None