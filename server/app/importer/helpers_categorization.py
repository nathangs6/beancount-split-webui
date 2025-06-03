from app.importer.types_beancount import JSONTransaction
from app.config.config_services import get_key_rules
from ..env import USER_1_NAME, USER_2_NAME

def determine_duplicates(transaction: JSONTransaction, beancount_lines: list[str]) -> None:
    """
    Checks if a transaction is a duplicate of any transaction in the beancount file
    """
    try:
        # Read the file in reverse order
        for line in reversed(beancount_lines):
            if (transaction.transaction_date in line and
                transaction.description in line and
                transaction.extended_description in line):
                transaction.is_duplicate = True
                return 
    except Exception as e:
        print(f"An error occurred: {e}")

def apply_key_rule_categorization(transactions: JSONTransaction):
    """
    Apply key rule categorization to a list of transactions.
    
    Args:
        transactions (JSONTransaction): List of transactions to categorize.
    
    """

    try:
        rules = get_key_rules()["keyrules"]
    except Exception as e:
        raise Exception(f"Error reading key rules configuration: {str(e)}")
    for transaction in transactions:
        for rule_key in rules:
            rule = rules[rule_key]
            if rule["type"] == "description":
                if rule["key"] in transaction.description.lower():
                    if transaction.plus_account == "":
                        transaction.plus_account = rule["plus_account"]
                    if transaction.minus_account == "":
                        transaction.minus_account = rule["minus_account"]
                    if transaction.shared_percentages == {} and rule["shared_percentages"] is not None:
                        transaction.shared_percentages = {
                            USER_1_NAME: rule["shared_percentages"][0],
                            USER_2_NAME: rule["shared_percentages"][1],
                        }
