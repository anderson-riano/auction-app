from fastapi import APIRouter
from app.database.crud import *
from app.schemas.item import ItemCreate, ItemResponse
from datetime import datetime, timedelta
from typing import List
import uuid

router = APIRouter()

@router.post("/", response_model=ItemResponse)
def create_new_item(item: ItemCreate):
    now = datetime.utcnow()
    expires_at = now + timedelta(minutes=item.minutes)

    item_data = item.dict()
    item_data.update({
        "id": str(uuid.uuid4()),
        "created_at": now.isoformat(),  # Formato compatible con DynamoDB
        "expires_at": expires_at.isoformat(),
        "status": "active"
    })

    saved_item = create_item(item_data)
    return saved_item

@router.get("/active/", response_model=List[ItemResponse])
def get_existing_items():
    return get_all_active_items()

@router.get("/", response_model=List[ItemResponse])
def get_existing_items():
    return get_all_items()

@router.get("/{item_id}", response_model=ItemResponse)
def get_existing_item(item_id: str):
    return get_item(item_id)
