# Import TestClient → used to simulate API requests (like a fake user)
from fastapi.testclient import TestClient

# Import your FastAPI app → this is the actual backend application
from main import app

# Import status codes → cleaner way to use HTTP status (like 200, 404)
from fastapi import status


# Create a client instance
# 👉 This acts like a user (browser/Postman) sending requests to your API
client = TestClient(app)


# Test function (pytest detects this because of "test_" prefix)
def test_return_health_check():
    
    # 🔹 Send a GET request to "/healthy" endpoint
    # 👉 Simulates: user calling your API
    response = client.get("/healthy")
    

    # 🔹 Check if response status code is 200 (OK)
    # 👉 Ensures API is working correctly
    assert response.status_code == status.HTTP_200_OK
    

    # 🔹 Check if response body (JSON) is correct
    # 👉 Ensures API returns expected data
    assert response.json() == {'status': 'Healthy'}



