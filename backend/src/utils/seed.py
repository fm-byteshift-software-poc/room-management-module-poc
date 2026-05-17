from sqlalchemy.orm import Session
from src.models.room_type import RoomType
from src.models.room import Room, RoomStatus
from src.config.database import SessionLocal

def run_seed():
    """Initializes database with seed data if tables are empty."""
    with SessionLocal() as db:
        # Skip seeding if rooms already exist (prevents duplicates on hot reload)
        if db.query(Room).count() > 0:
            return

        # 1. Seed Room Types (2 records)
        standard = RoomType(name="Standard", description="Room with one double bed, capacity up to 2 guests")
        suite = RoomType(name="Suite", description="Room with separate living area, capacity up to 4 guests")
        db.add_all([standard, suite])
        db.flush()  # Flush to generate IDs before creating rooms

        # 2. Seed Rooms (5 records with exact status distribution)
        rooms_data = [
            Room(number="101", floor=1, capacity=2, status=RoomStatus.available, room_type_id=standard.id),
            Room(number="102", floor=1, capacity=2, status=RoomStatus.occupied, room_type_id=standard.id),
            Room(number="201", floor=2, capacity=4, status=RoomStatus.available, room_type_id=suite.id),
            Room(number="202", floor=2, capacity=4, status=RoomStatus.maintenance, room_type_id=suite.id),
            Room(number="103", floor=1, capacity=2, status=RoomStatus.inactive, room_type_id=standard.id),
        ]
        db.add_all(rooms_data)
        db.commit()