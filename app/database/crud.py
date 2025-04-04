from app.database.connection import items_table, bids_table
from botocore.exceptions import ClientError
from datetime import datetime, timezone
from decimal import Decimal
from fastapi import HTTPException
from collections import Counter
import uuid

def create_item(item_data):
    try:
        items_table.put_item(Item=item_data)
        return item_data
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return None

def get_item(item_id):
    try:
        response = items_table.get_item(Key={"id": item_id})
        return response.get("Item", {})
    except ClientError as e:
        return {"error": str(e)}


def get_all_items():
    try:
        response = items_table.scan()
        return response.get("Items", []) 
    except ClientError as e:    
        return {"error": e.response["Error"]["Message"]} 
    
def get_all_active_items():
    try:
        now = datetime.utcnow().isoformat()
        response = items_table.scan(
            FilterExpression="expires_at > :now",
            ExpressionAttributeValues={":now": now}
        )
        return response.get("Items", [])
    except ClientError as e:
        return {"error": e.response["Error"]["Message"]}    

def create_bid(bid_data):
    item = get_item(bid_data["item_id"])
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    expires_at = datetime.fromisoformat(item["expires_at"]).replace(tzinfo=timezone.utc)
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    
    if now >= expires_at:
        raise HTTPException(status_code=400, detail="Item expired")
    
    if bid_data["user_email"] == item["user_email"]:
        raise HTTPException(status_code=400, detail="Same user")
    
    starting_price = Decimal(str(item["starting_price"]))
    current_price = Decimal(str(item.get("current_price", "0.00")))
    
    if current_price == Decimal("0.00"):
        if bid_data["amount"] < starting_price:
            raise HTTPException(status_code=400, detail=f"The amount the amount must be at least equal to {starting_price}")
    else:
        if bid_data["amount"] <= current_price:
            raise HTTPException(status_code=400, detail=f"The amount is not greater than {current_price}")
        
    bid_data["created_at"] = datetime.utcnow().isoformat()

    try:
        bids_table.put_item(Item=bid_data)

        update_item_price(bid_data["item_id"], bid_data["id"], bid_data["amount"])
        
        return bid_data
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])

def update_item_price(item_id, bid_id, new_price):
    try:
        items_table.update_item(
            Key={"id": item_id},
            UpdateExpression="SET bid_id = :new_bid_id, current_price = :new_price ",
            ExpressionAttributeValues={":new_price": Decimal(str(new_price)), ":new_bid_id": bid_id}
        )
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])
    
def get_top_bidders():
    closed_items = items_table.scan(
        FilterExpression="#status = :closed",
        ExpressionAttributeNames={"#status": "status"},
        ExpressionAttributeValues={":closed": "closed"}
    )["Items"]
    
    winner_emails = []

    for item in closed_items:
        bid_id = item.get("bid_id")
        if bid_id:
            bid = bids_table.get_item(Key={"id": bid_id}).get("Item")
            if bid and "user_email" in bid:
                winner_emails.append(bid["user_email"])
    
    counts = Counter(winner_emails)
    top_five = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]

    return [{"email": email, "wins": wins} for email, wins in top_five]