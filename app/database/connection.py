import boto3
from app.core.config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

items_table = dynamodb.Table("AuctionAppStack-ItemsTable5AAC2C46-SBSP6TXX75G1")
bids_table = dynamodb.Table("AuctionAppStack-BidsTableE1AD1632-14HE7UVGQNPYW")
