from datetime import datetime
from fastapi.testclient import TestClient
import os

from ...main import app
from ...env import SHARED_NAME, INDENT_STRING, USERS_LIST

client = TestClient(app)

def test_upload():
    fp = os.path.join(os.path.dirname(__file__), "example_data.csv")
    with open(fp, "rb") as f:
        response = client.post("/importer/upload/Bob", files={"file": f})
    assert response.status_code == 200
    actual = response.json()
    assert isinstance(actual, list)
    expected = [
                    {
                      "account_type": "Visa",
                      "account_number": "123",
                      "plus_account": "Expenses:Food:Groceries",
                      "minus_account": "",
                      "transaction_date": "2025-01-06",
                      "description": "Sobeys",
                      "extended_description": "",
                      "amount": -30.0,
                      "shared_percentages": {
                        "Bob": 50.0,
                        "Joe": 50.0
                      },
                      "is_duplicate": True
                    },
                    {
                      "account_type": "Visa",
                      "account_number": "123",
                      "plus_account": "Expenses:House",
                      "minus_account": "",
                      "transaction_date": "2025-01-07",
                      "extended_description": "",
                      "description": "Bell",
                      "amount": -55.23,
                      "shared_percentages": {},
                      "is_duplicate": True
                    },
                    {
                      "account_type": "Visa",
                      "account_number": "123",
                      "plus_account": "",
                      "minus_account": "",
                      "transaction_date": "2025-01-10",
                      "description": "Spotify",
                      "extended_description": "",
                      "amount": -9.82,
                      "shared_percentages": {},
                      "is_duplicate": False
                    },
                    {
                        "account_type": "Savings",
                        "account_number": "456",
                        "plus_account": "",
                        "minus_account": "",
                        "transaction_date": "2025-02-10",
                        "description": "Job",
                        "extended_description": "",
                        "amount": 100.0,
                        "shared_percentages": {},
                        "is_duplicate": False
                    },
                    {
                        "account_type": "Visa",
                        "account_number": "123",
                        "plus_account": "",
                        "minus_account": "",
                        "transaction_date": "2025-01-24",
                        "description": "Electronics",
                        "extended_description": "",
                        "amount": -24.0,
                        "shared_percentages": {},
                        "is_duplicate": False
                    }
                ]
    for i in range(len(actual)):
        print(f"Expected: {expected[i]}")
        print(f"Actual  : {actual[i]}")
    assert actual == expected


def test_validate_success():
    USER_1_NAME = USERS_LIST[0]["name"]
    USER_2_NAME = USERS_LIST[1]["name"]
    request = [
        {
            "account_type": "Visa",
            "account_number": "123",
            "plus_account": "Expenses:Food:Groceries",
            "minus_account": "Assets:Bank:Chequing",
            "transaction_date": "2025-01-06",
            "description": "Sobeys",
            "extended_description": "Oreos",
            "amount": -30.00,
            "shared_percentages": {
                USER_1_NAME: 50,
                USER_2_NAME: 50
            },
            "is_duplicate": False
        },
        {
            "account_type": "Visa",
            "account_number": "123",
            "plus_account": "Expenses:House",
            "minus_account": "Assets:Bank:Chequing",
            "transaction_date": "2025-01-07",
            "description": "Bell",
            "extended_description": "",
            "amount": -55.23,
            "shared_percentages": {
                USER_1_NAME: 50,
                USER_2_NAME: 50
            },
            "is_duplicate": False
        },
        {
            "account_type": "Visa",
            "account_number": "123",
            "plus_account": "Expenses:Food:Groceries",
            "minus_account": "Assets:Bank:Chequing",
            "transaction_date": "2025-01-06",
            "description": "Shoppers",
            "extended_description": "",
            "amount": -11.24,
            "shared_percentages": {
                USER_1_NAME: 50,
                USER_2_NAME: 50
            },
            "is_duplicate": True
        }
    ]
    response = client.post("/importer/validate/"+USER_1_NAME, json=request)
    print(response.status_code)
    assert response.status_code == 200
    actual = response.json()
    assert isinstance(actual, dict)
    assert "message" in actual
    assert actual["message"] == "Transactions are valid"
    assert "transaction_strings" in actual
    ts = actual["transaction_strings"]
    assert isinstance(ts, dict)
    print("Testing")
    expected = f"""; Imported by: {USER_1_NAME}, on: {datetime.today().strftime('%Y-%m-%d')}

2025-01-06 * "Sobeys" "Oreos"
{INDENT_STRING}Expenses:Food:Groceries 30.00 CAD
{INDENT_STRING}Assets:Bank:Chequing -30.00 CAD

2025-01-06 * "Reimbursement: Sobeys" "Oreos" #{SHARED_NAME}
{INDENT_STRING}Expenses:Food:Groceries:{SHARED_NAME} -15.00 CAD
{INDENT_STRING}Equity:{USER_2_NAME} 15.00 CAD

2025-01-07 * "Bell" ""
{INDENT_STRING}Expenses:House 55.23 CAD
{INDENT_STRING}Assets:Bank:Chequing -55.23 CAD

2025-01-07 * "Reimbursement: Bell" "" #{SHARED_NAME}
{INDENT_STRING}Expenses:House:{SHARED_NAME} -27.61 CAD
{INDENT_STRING}Equity:{USER_2_NAME} 27.61 CAD"""
    expected_split = expected.split("\n")
    actual_split = ts[USER_1_NAME].split("\n")
    for i in range(len(expected_split)):
        if (expected_split[i] == actual_split[i]):
            continue
        print(f"Expected: {expected_split[i]}")
        print(f"Actual  : {actual_split[i]}")
    assert ts[USER_1_NAME] == expected

    expected = f"""; Imported by: {USER_1_NAME}, on: {datetime.today().strftime('%Y-%m-%d')}

2025-01-06 * "Reimbursement: Sobeys" "Oreos" #{SHARED_NAME}
{INDENT_STRING}Expenses:Food:Groceries:{SHARED_NAME} 15.00 CAD
{INDENT_STRING}Equity:{USER_1_NAME} -15.00 CAD

2025-01-07 * "Reimbursement: Bell" "" #{SHARED_NAME}
{INDENT_STRING}Expenses:House:{SHARED_NAME} 27.61 CAD
{INDENT_STRING}Equity:{USER_1_NAME} -27.61 CAD"""
    assert ts[USER_2_NAME] == expected
