import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

@pytest.fixture
def new_item():
    response = client.post("/items/", json={
        "name": "Laptop Dell",
        "description": "Laptop usada en buen estado",
        "starting_price": 500,
        "user_email": "seller@test.com",
        "minutes": 10
    })
    assert response.status_code == 200
    return response.json()

def test_create_item():
    response = client.post("/items/", json={
        "name": "PlayStation 5",
        "description": "Nueva en caja",
        "starting_price": 800,
        "user_email": "user@test.com",
        "minutes": 30
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "PlayStation 5"
    assert data["status"] == "active"

def test_valid_bid(new_item):
    response = client.post("/bids/", json={
        "item_id": new_item["id"],
        "user_email": "bidder1@test.com",
        "amount": 900
    })
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 900

def test_bid_lower_than_starting_price(new_item):
    response = client.post("/bids/", json={
        "item_id": new_item["id"],
        "user_email": "bidder2@testt.com",
        "amount": 100  
    })
    assert response.status_code == 400 or response.status_code == 403
    assert "menor al precio inicial" in response.text.lower()

def test_bid_by_creator(new_item):
    response = client.post("/bids/", json={
        "item_id": new_item["id"],
        "user_email": "seller@test.com",  
        "amount": 1000
    })
    assert response.status_code == 400 or response.status_code == 403
    assert "no puede pujar" in response.text.lower()

def test_get_winner(new_item):
    client.post("/bids/", json={
        "item_id": new_item["id"],
        "user_email": "ganador@test.com",
        "amount": 1000
    })

    response = client.get(f"/bids/winner/{new_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_email"] == "ganador@test.com"
