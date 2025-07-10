from app.importer.types_beancount import Transaction
from app.config.config_services import get_key_rules
from ..env import USERS_LIST

def determine_duplicates(transactions: list[Transaction], beancount: list[str]) -> None:
    """
    Checks if a transaction is a duplicate of any transaction in the beancount file
    """
    for transaction in transactions:
        # Read the file in reverse order
        for line in reversed(beancount):
            if (transaction.transaction_date in line and
                transaction.description in line and
                transaction.extended_description in line):
                transaction.is_duplicate = True
                break

def apply_key_rule_categorization(transactions: list[Transaction], owner: str):
    """
    Apply key rule categorization to a list of transactions.
    
    Args:
        transactions (JSONTransaction): List of transactions to categorize.
    
    """

    try:
        rules = get_key_rules(owner)["keyrules"]
        print(rules)
    except Exception as e:
        raise Exception(f"Error reading key rules configuration: {str(e)}")
    for transaction in transactions:
        for rule_key in rules:
            rule = rules[rule_key]
            if rule["type"] == "description":
                if rule["key"] in transaction.description.lower():
                    transaction.plus_account = rule["plus_account"]
                    transaction.minus_account = rule["minus_account"]
                    if rule["shared_percentages"] is not None:
                        transaction.shared_percentages = {
                            USERS_LIST[0]["name"]: rule["shared_percentages"][0],
                            USERS_LIST[1]["name"]: rule["shared_percentages"][1],
                        }
