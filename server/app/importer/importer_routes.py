from fastapi import APIRouter, File, HTTPException, UploadFile
import csv
from io import StringIO

from ..env import USER_1_NAME, USER_2_NAME, USER_1_BEANCOUNT_FILE, USER_2_BEANCOUNT_FILE

from .types_beancount import FromBankTransaction, JSONTransaction

from .importer_services import process_uploaded_file, generate_beancount_entries, update_beancount_file, validate_transactions, determine_duplicates


router = APIRouter(prefix="/importer", tags=["importer"])

@router.post("/upload")
async def upload(file: UploadFile = File(...)) -> list[FromBankTransaction]:
    try:
        contents = await file.read()
        ret = process_uploaded_file(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    finally:
        await file.close()
    return ret


@router.post("/determine_duplicates/{owner}")
async def determine_duplicates_endpoint(
    owner: str, transactions: list[JSONTransaction]
):
    try:
        if owner == USER_1_NAME:
            beancount_file_path = USER_1_BEANCOUNT_FILE
        elif owner == USER_2_NAME:
            beancount_file_path = USER_2_BEANCOUNT_FILE
        else:
            raise HTTPException(
                status_code=400, detail="Invalid owner. Must be USER_1 or USER_2."
            )
        with open(beancount_file_path, "r") as file:
            beancount_data = file.readlines()
        for transaction in transactions:
            determine_duplicates(transaction, beancount_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error determining duplicates: {str(e)}")
    return {"message": "Duplicates determined successfully", "transactions": transactions}


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
