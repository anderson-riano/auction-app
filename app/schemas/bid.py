from pydantic import BaseModel, EmailStr, condecimal
from datetime import datetime

class BidCreate(BaseModel):
    item_id: str
    user_email: EmailStr
    amount: condecimal(max_digits=10, decimal_places=2)

class BidResponse(BidCreate):
    id: str
    created_at: datetime