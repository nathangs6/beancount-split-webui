from fastapi import APIRouter, HTTPException
from .bean_accounts import get_bean_accounts

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/{owner}")
async def get_accounts(owner: str):
    """
    Returns a list of accounts.
    """
    try:
        accounts = get_bean_accounts(owner)
        return {"accounts": accounts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
