from fastapi import APIRouter
from app.database.crud import create_bid, get_top_bidders
from app.schemas.bid import BidCreate, BidResponse
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/", response_model=BidResponse)
def place_new_bid(bid: BidCreate):
    now = datetime.utcnow()
    
    bid_data = bid.dict()    
    bid_data.update({
        "id": str(uuid.uuid4()),
        "created_at": now.isoformat()
    })
    
    return create_bid(bid_data)

@router.get("/top-bidders/")
def top_bidders():
    return get_top_bidders()