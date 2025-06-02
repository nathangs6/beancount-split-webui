from fastapi.testclient import TestClient

from ...main import app
from ...config.categorization import apply_key_rule_categorization
from ...importer.beancount_types import JSONTransaction

client = TestClient(app)


def test_rule_based():
    request = [
        {
            "plus_account": "",
            "minus_account": "Assets:Bank:Chequing",
            "transaction_date": "2025-01-06",
            "description": "Sobeys",
            "extended_description": "Oreos",
            "amount": -30.00,
            "shared_percentages": {},
            "is_duplicate": False
        },
        {
            "plus_account": "",
            "minus_account": "Assets:Bank:Chequing",
            "transaction_date": "2025-01-07",
            "description": "Bell",
            "extended_description": "",
            "amount": -55.23,
            "shared_percentages": {},
            "is_duplicate": False
        },
        {
            "plus_account": "",
            "minus_account": "Assets:Bank:Chequing",
            "transaction_date": "2025-01-06",
            "description": "Shoppers",
            "extended_description": "",
            "amount": -11.24,
            "shared_percentages": {},
            "is_duplicate": True
        }
    ]
    transactions = []
    for transaction in request:
        transactions.append(JSONTransaction(**transaction))
    
    apply_key_rule_categorization(transactions)
    assert transactions[0].plus_account == "Expenses:Food:Groceries"
    assert transactions[0].minus_account == "Assets:Bank:Chequing"
    assert transactions[0].shared_percentages == {
        "Bob": 50,
        "Joe": 50
    }
    assert transactions[1].plus_account == "Expenses:House"
    assert transactions[1].minus_account == "Assets:Bank:Chequing"
    assert transactions[2].plus_account == ""
    assert transactions[2].minus_account == "Assets:Bank:Chequing"
