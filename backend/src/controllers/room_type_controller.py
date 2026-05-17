from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.config.database import get_db
from src.schemas.room import RoomTypeSchema
from src.services import room_type_service

router = APIRouter()

@router.get("/", response_model=List[RoomTypeSchema])
def list_room_types(db: Session = Depends(get_db)):
    return room_type_service.get_all_room_types(db)