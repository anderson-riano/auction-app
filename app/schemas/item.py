from pydantic import BaseModel, condecimal, EmailStr
from decimal import Decimal
from datetime import datetime
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: str
    starting_price: condecimal(max_digits=10, decimal_places=2)
    current_price: Optional[condecimal(max_digits=10, decimal_places=2)] = Decimal("0.00")
    user_email: EmailStr
    minutes: int  # Tiempo hasta que expire

class ItemResponse(ItemCreate):
    id: str
    created_at: datetime
    expires_at: datetime
    status: str  # active, closed
    bid_id: Optional[str] = None 
