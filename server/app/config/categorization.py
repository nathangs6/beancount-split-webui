from server.app.importer.beancount_types import JSONTransaction


def apply_key_rule_categorization(transactions: JSONTransaction):
    """
    Apply key rule categorization to a list of transactions.
    
    Args:
        transactions (JSONTransaction): List of transactions to categorize.
    
    Returns:
        JSONTransaction: Categorized transactions.
    """
    from ..config.config_services import ConfigServices

    services = ConfigServices()
    try:
        rules = services.get_key_rules()
    except Exception as e:
        raise Exception(f"Error reading key rules configuration: {str(e)}")

    categorized_transactions = []
    for transaction in transactions:
        category = "Uncategorized"
        for rule in rules.get("rules", []):
            if rule["key"] in transaction.get("description", ""):
                category = rule["category"]
                break
        transaction["category"] = category
        categorized_transactions.append(transaction)

    return categorized_transactions
