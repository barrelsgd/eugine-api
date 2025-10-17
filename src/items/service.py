import uuid

from sqlmodel import Session, select

from .models import Item, ItemImage
from .schemas import ItemCreate, ItemImageCreate


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    """Create a new item."""
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_item_image(
    *, session: Session, item_id: uuid.UUID, image_in: ItemImageCreate
) -> ItemImage:
    """Create a new item image."""
    db_image = ItemImage.model_validate(image_in, update={"item_id": item_id})
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return db_image


def get_item_images(*, session: Session, item_id: uuid.UUID) -> list[ItemImage]:
    """Get all images for an item."""
    statement = select(ItemImage).where(ItemImage.item_id == item_id)
    return list(session.exec(statement).all())
