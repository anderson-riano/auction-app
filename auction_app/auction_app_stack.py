from aws_cdk import Stack
import aws_cdk.aws_dynamodb as dynamodb
from constructs import Construct

class AuctionAppStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.items_table = dynamodb.Table(
            self, "ItemsTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        self.bids_table = dynamodb.Table(
            self, "BidsTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
