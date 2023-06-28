import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import main
from database import SessionLocal, engine

# Create a test database
main.models.Base.metadata.create_all(bind=engine)

# Override the dependency function to use a test database
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

main.get_db = override_get_db

# Test the "/Prices_all/" endpoint
def test_read_prices():
    client = TestClient(main.app)
    response = client.get("/Prices_all/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test the "/Prices/{Filter_date}" endpoint
def test_read_price():
    client = TestClient(main.app)
    response = client.get("/Prices/2023-06-28")
    assert response.status_code == 404  # Assuming the data for the given date is not available in the test database

# Test the "/Predictions_all/" endpoint
def test_read_predictions():
    client = TestClient(main.app)
    response = client.get("/Predictions_all/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Run the tests
def run_tests():
    test_read_prices()
    test_read_price()
    test_read_predictions()

run_tests()
