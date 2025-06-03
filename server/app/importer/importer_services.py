import csv
from io import StringIO
from typing import List, Dict
from datetime import datetime
from beancount import loader
from .types_beancount import Transaction
from ..env import INDENT_STRING, SHARED_NAME, USER_1_NAME, USER_1_BEANCOUNT_FILE, USER_2_NAME, USER_2_BEANCOUNT_FILE
from ..config.config_services import get_csv_column_mapping
from .helpers_categorization import determine_duplicates, apply_key_rule_categorization

#####################
### FILE HANDLING ###
#####################
def init_transactions(contents: bytes) -> List[Transaction]:
    """
    Given an uploaded file containing bytes content contents, process the file
    and return a list of initialized transactions.
    Input:
        - contents (bytes): the uploaded file
    Output: A list of initialized Transaction
    """
    # Get the column mapping
    columns = get_csv_column_mapping()
    # Then, read the file and create the transaction list
    buffer = StringIO(contents.decode("utf-8"))
    reader = csv.reader(buffer)
    next(reader)
    transactions = []
    for row in reader:
        transaction = Transaction(
            account_type=row[columns["account_type"]],
            account_number=row[columns["account_number"]],
            plus_account="",
            minus_account="",
            transaction_date=row[columns["transaction_date"]],
            description=row[columns["description"]],
            extended_description="",
            amount=float(row[columns["amount"]]),
            shared_percentages={},
            is_duplicate=False
        )
        transaction.transaction_date = datetime.strptime(transaction.transaction_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        transactions.append(transaction)
    return transactions

def load_beancount_file(owner: str):
    if owner == USER_1_NAME:
        fp = USER_1_BEANCOUNT_FILE
    elif owner == USER_2_NAME:
        fp = USER_2_BEANCOUNT_FILE
    else:
        raise Exception("Owner not valid!")
    try:
        with open(fp, "r") as file:
            beancount_data = file.readlines()
    except Exception as e:
        raise Exception(f"Error reading beancount file: {e}")
    return beancount_data

def process_uploaded_file(owner: str, contents: bytes) -> List[Transaction]:
    """
    Processes the uploaded file and returns a list of JSONTransaction objects
    """
    transactions = init_transactions(contents)
    # Next, load the beancount file
    beancount = load_beancount_file(owner)
    # Now, apply the varying pre-processing methods for the transactions
    determine_duplicates(transactions, beancount)
    apply_key_rule_categorization(transactions)
    return transactions


######################
### PRE-PROCESSING ###
######################
def preprocess_transactions(transactions: List[Transaction]) -> None:
    """
    Pre-processes the FromBankTransaction objects into JSONTransaction objects
    """
    json_transactions = []
    for transaction in transactions:
        json_transaction = JSONTransaction(
            plus_account="",
            minus_account="",
            transaction_date=transaction.transaction_date,
            description=transaction.description,
            extended_description="",
            amount=transaction.amount,
            shared_percentages={},
            is_duplicate=False
        )
        json_transactions.append(json_transaction)
    return json_transactions


##################
### VALIDATION ###
##################
def validate_transaction(transaction: Transaction) -> bool:
    """
    Validates the JSONTransaction object
    """
    if not transaction.transaction_date:
        return False
    if not transaction.description:
        return False
    if not transaction.amount:
        return False
    if not transaction.plus_account:
        return False
    if not transaction.minus_account:
        return False
    return True

def validate_transactions(transactions: List[Transaction]) -> bool:
    """
    Validates a list of JSONTransaction objects
    """
    for transaction in transactions:
        if not transaction.is_duplicate and not validate_transaction(transaction):
            return False
    return True
    

##################
### GENERATION ###
##################
def generate_beancount_entry(transaction: Transaction, owner: str) -> Dict[str,str]:
    """
    Generates (potentially) multiple beancount entries from the JSONTransaction object
    """
    result = {}

    date = transaction.transaction_date
    description = transaction.description
    extended_description = transaction.extended_description
    orig_amount = transaction.amount
    plus_account = transaction.plus_account
    minus_account = transaction.minus_account
    shared_percentages = transaction.shared_percentages

    entry = f"""{date} * "{description}" "{extended_description}"
{INDENT_STRING}{plus_account} {abs(orig_amount):.2f} CAD
{INDENT_STRING}{minus_account} {-abs(orig_amount):.2f} CAD"""
    result[owner] = entry
    for person, percentage in shared_percentages.items():
        if percentage == 0:
            continue
        if person == owner:
            continue

        amount = round(orig_amount * percentage/100, 2)
        if amount > 0:  # this is like income
            shared_account = minus_account
            amount = abs(amount)
        else:
            shared_account = plus_account
            amount = -abs(amount)
        # Handle Owner entry
        entry = f"{date} * \"Reimbursement: {description}\" \"{extended_description}\" #{SHARED_NAME}\n"
        entry += f"{INDENT_STRING}{shared_account}:{SHARED_NAME} {amount:.2f} CAD\n"
        entry += f"{INDENT_STRING}Equity:{person} {-amount:.2f} CAD"
        result[owner] += "\n\n" + entry

        # Handle Person entry
        entry = f"{date} * \"Reimbursement: {description}\" \"{extended_description}\" #{SHARED_NAME}\n"
        entry += f"{INDENT_STRING}{shared_account}:{SHARED_NAME} {-amount:.2f} CAD\n"
        entry += f"{INDENT_STRING}Equity:{owner} {amount:.2f} CAD"
        result[person] = entry
    return result

def generate_beancount_entries(transactions: List[Transaction], owner: str) -> Dict[str, str]:
    """
    Generates beancount entries from a list of JSONTransaction objects
    """
    result = {}
    for transaction in transactions:
        if transaction.is_duplicate:
            continue
        entries = generate_beancount_entry(transaction, owner)
        for person, entry in entries.items():
            if person not in result:
                result[person] = []
            result[person].append(entry)
    for person in result:
        result[person] = "\n\n".join(result[person])
    for person in result:
        result[person] = "; Imported by: " + owner + ", on: " + datetime.today().strftime("%Y-%m-%d") + "\n\n" + result[person]
    return result

##################
### Submission ###
##################
def update_beancount_file(new_entries: Dict[str, str]) -> None:
    """
    Updates the beancount file with the new entries
    """
    for owner, entry in new_entries.items():
        if owner == USER_1_NAME:
            beancount_file_path = USER_1_BEANCOUNT_FILE
        else:
            beancount_file_path = USER_2_BEANCOUNT_FILE
        with open(beancount_file_path, "r") as f:
            bean_text = f.read()
        bean_text += "\n\n" + entry
        (entries, errors, options) = loader.load_string(bean_text)
        print(entries)
        print(errors)
        print(options)
        if len(errors) > 0:
            print("Errors in beancount file:")
            for error in errors:
                print(error)
            raise Exception("Errors in beancount file")
        with open(beancount_file_path, "a") as f:
            f.write("\n\n" + entry)
