import os
from aws_cdk import App, Environment
from auction_app.auction_app_stack import AuctionAppStack
from auction_app.fastapi_stack import FastApiStack

app = App()


env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION")
)

auction_stack = AuctionAppStack(app, "AuctionAppStack", env=env)

FastApiStack(
    app, "FastApiStack",
    items_table=auction_stack.items_table,
    bids_table=auction_stack.bids_table,
    env=env
)

app.synth()
