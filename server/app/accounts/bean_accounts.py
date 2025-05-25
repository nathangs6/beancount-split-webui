from fastapi import HTTPException
from ..env import USER_1_BEANCOUNT_FILE, USER_2_BEANCOUNT_FILE, SHARED_NAME, USER_1_NAME, USER_2_NAME

def get_bean_accounts(owner: str):
    """
    Returns a list of accounts.
    """
    try:
        accounts = []
        account_flag = False
        beanfile = USER_1_BEANCOUNT_FILE if owner == USER_1_NAME else USER_2_BEANCOUNT_FILE
        other_user = USER_2_NAME if owner == USER_1_NAME else USER_1_NAME
        print(beanfile)
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
