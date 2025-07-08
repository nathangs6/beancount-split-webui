from fastapi import APIRouter, HTTPException
from ..env import USERS_LIST

router = APIRouter(prefix="/users", tags=["users"])
@router.get("/")
async def get_users():
    """
    Returns a list of users.
    """
    try:
        users = [USERS_LIST[0]["name"], USERS_LIST[1]["name"]]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unknown error occured: {str(e)}")

