from fastapi import FastAPI
from app.routes import items, bids

app = FastAPI(title="Auction API", version="1.1")

app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(bids.router, prefix="/bids", tags=["Bids"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Auction API"}
