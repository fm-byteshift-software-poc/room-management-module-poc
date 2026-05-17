from uuid import UUID
from datetime import datetime, timezone

from src.models.item import Item, ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self):
        self._db: dict[UUID, Item] = {}

    def get_all(self) -> list[Item]:
        return list(self._db.values())

    def get_by_id(self, item_id: UUID) -> Item | None:
        return self._db.get(item_id)

    def create(self, payload: ItemCreate) -> Item:
        item = Item(**payload.model_dump())
        self._db[item.id] = item
        return item

    def update(self, item_id: UUID, payload: ItemUpdate) -> Item | None:
        item = self._db.get(item_id)
        if not item:
            return None

        updated_data = payload.model_dump(exclude_unset=True)
        updated_data["updated_at"] = datetime.now(timezone.utc)

        updated_item = item.model_copy(update=updated_data)
        self._db[item_id] = updated_item
        return updated_item

    def delete(self, item_id: UUID) -> bool:
        if item_id not in self._db:
            return False
        del self._db[item_id]
        return True


# Singleton pattern — provides a shared in-memory store across the application lifecycle
item_repository = ItemRepository()
