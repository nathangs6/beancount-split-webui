from fastapi.testclient import TestClient

from ...main import app

client = TestClient(app)

def test_get_accounts():
    response = client.get("/accounts/Bob")
    print(response.json())
    assert response.status_code == 200
    assert "accounts" in response.json()
    actual_accounts = response.json()["accounts"]
    assert isinstance(actual_accounts, list)
    expected_accounts = [
        "Assets:Bank:Chequing",
        "Assets:Bank:Savings",
        "Liabilities:CreditCard",
        "Expenses:Food:Groceries",
        "Expenses:House",
        "Expenses:Rent",
        "Expenses:Hobbies",
        "Income:Salary"
    ]
    print("Actual  :", actual_accounts)
    print("Expected:", expected_accounts)
    assert response.json()["accounts"] == expected_accounts
