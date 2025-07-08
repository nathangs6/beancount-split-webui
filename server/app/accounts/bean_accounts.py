from fastapi import HTTPException
from ..env import USERS, USERS_LIST, SHARED_NAME

def get_bean_accounts(owner: str):
    """
    Returns a list of accounts.
    """
    try:
        if owner not in USERS:
            raise ValueError(f"Invalid owner: {owner}.")
        accounts = []
        account_flag = False
        beanfile = USERS[owner]["beancount_file"]
        other_user = USERS_LIST[0]["name"] if owner == USERS_LIST[1]["name"] else USERS_LIST[1]["name"]
        with open(beanfile, mode='r') as f:
            contents = f.read()
        for line in contents.splitlines():
            if line.strip() == "; Open accounts":
                account_flag = True
                continue
            if account_flag:
                if line == "":
                    break
                if SHARED_NAME in line or "Equity:"+other_user in line:
                    continue
                account = line.split(" ")[2]
                accounts.append(account)
        return accounts
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading file: {str(e)}")
