from fastapi import APIRouter, HTTPException
from ..env import USER_1_NAME, USER_2_NAME

router = APIRouter(prefix="/users", tags=["users"])
@router.get("/")
async def get_users():
    """
    Returns a list of users.
    """
    try:
        users = [USER_1_NAME, USER_2_NAME]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unknown error occured: {str(e)}")

