import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
DYNAMODB_ITEMS_TABLE = os.getenv("DYNAMODB_ITEMS_TABLE", "AuctionAppStack-ItemsTable")
DYNAMODB_BIDS_TABLE = os.getenv("DYNAMODB_BIDS_TABLE", "AuctionAppStack-BidsTable")