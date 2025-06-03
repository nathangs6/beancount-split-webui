# Define Pydantic models
from pydantic import BaseModel


class FromBankTransaction(BaseModel):
    account_type: str
    account_number: str
    transaction_date: str
    description: str
    amount: float

class JSONTransaction(BaseModel):
    plus_account: str
    minus_account: str
    transaction_date: str
    description: str
    extended_description: str
    amount: float
    shared_percentages: dict[str, float]
    is_duplicate: bool = False
