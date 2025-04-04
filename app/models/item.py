from pydantic import BaseModel, condecimal, EmailStr
from datetime import datetime, timedelta

class Item(BaseModel):
    id: str
    name: str
    description: str
    starting_price: condecimal(max_digits=10, decimal_places=2)
    current_price: condecimal(max_digits=10, decimal_places=2)
    user_email: EmailStr
    bid_id: str
    created_at: datetime
    expires_at: datetime
    status: str  # active, closed