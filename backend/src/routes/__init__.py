from fastapi import APIRouter
from src.controllers import room_controller, room_type_controller

# Root router aggregating all sub-routers
router = APIRouter()

# Mounting controllers
router.include_router(room_type_controller.router, prefix="/room-types", tags=["Room Types"])
router.include_router(room_controller.router, prefix="/rooms", tags=["Rooms"])