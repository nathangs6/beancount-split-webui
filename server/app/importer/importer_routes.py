from fastapi import APIRouter, File, HTTPException, UploadFile
import csv
from io import StringIO

from ..env import USERS

from .types_beancount import Transaction

from .importer_services import process_uploaded_file, generate_beancount_entries, update_beancount_file, validate_transactions, determine_duplicates


router = APIRouter(prefix="/importer", tags=["importer"])

@router.post("/upload/{owner}")
async def upload(owner: str, file: UploadFile = File(...)) -> list[Transaction]:
    # First, determine if owner is a valid owner
    if owner not in USERS:
        raise HTTPException(
            status_code=400, detail="Invalid owner. Must be USER_1 or USER_2."
        )
    # Then, get uploaded file contents
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    finally:
        await file.close()
    # Finally, feed data to the service
    transactions = process_uploaded_file(owner, contents)
    return transactions

"""
@router.post("/validate/{owner}")
async def validate(owner: str, transactions: list[JSONTransaction]):
    try:
        valid = validate_transactions(transactions)
        if not valid:
            raise HTTPException(status_code=400, detail="Invalid transactions")
        entries = generate_beancount_entries(transactions, owner)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating transactions: {str(e)}")
    return {"message": "Transactions are valid", "transaction_strings": entries}


@router.post("/import")
async def import_transactions(entries: dict[str, str]):
    try:
        update_beancount_file(entries)
        return {"message": "Entries submitted successfully", "entries": entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing transactions: {str(e)}")
"""
