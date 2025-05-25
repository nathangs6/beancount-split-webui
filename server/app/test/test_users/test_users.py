from fastapi.testclient import TestClient

from ...main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert "users" in response.json()
    actual_users = response.json()["users"]
    assert isinstance(actual_users, list)
    expected_users = [
        "Bob",
        "Joe"
    ]
    print("Actual  :", actual_users)
    print("Expected:", expected_users)
    assert actual_users == expected_users
