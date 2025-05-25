import csv
from io import StringIO
from typing import List, Dict
from datetime import datetime
from beancount import loader
from .beancount_types import JSONTransaction, FromBankTransaction
from ..env import INDENT_STRING, SHARED_NAME, USER_1_NAME, USER_1_BEANCOUNT_FILE, USER_2_NAME, USER_2_BEANCOUNT_FILE

#####################
### FILE HANDLING ###
#####################
def process_uploaded_file(contents: bytes) -> List[FromBankTransaction]:
    """
    Processes the uploaded file and returns a list of JSONTransaction objects
    """
    buffer = StringIO(contents.decode("utf-8"))
    reader = csv.reader(buffer)
    next(reader)
    transactions = []
    for row in reader:
        transaction = FromBankTransaction(
            account_type=row[0],
            account_number=row[1],
            transaction_date=row[2],
            description=row[4],
            amount=float(row[6]),
        )
        transaction.transaction_date = datetime.strptime(transaction.transaction_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        transactions.append(transaction)
    return transactions


##################
### VALIDATION ###
##################
def validate_transaction(transaction: JSONTransaction) -> bool:
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

def validate_transactions(transactions: List[JSONTransaction]) -> bool:
    """
    Validates a list of JSONTransaction objects
    """
    for transaction in transactions:
        if not transaction.is_duplicate and not validate_transaction(transaction):
            print(transaction)
            return False
    return True

#########################
### DUPLICATION CHECK ###
#########################
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
    

##################
### GENERATION ###
##################
def generate_beancount_entry(transaction: JSONTransaction, owner: str) -> Dict[str,str]:
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

def generate_beancount_entries(transactions: List[JSONTransaction], owner: str) -> Dict[str, str]:
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
