from pydantic import BaseModel

class Bid(BaseModel):
    user_id: str
    item_id: str
    bid_amount: float
