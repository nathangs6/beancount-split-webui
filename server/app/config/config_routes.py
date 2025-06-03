from fastapi import APIRouter, HTTPException
from .config_services import get_key_rules

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/config/categorization")
async def get_categorization_config():
    """
    Returns the categorization configuration.
    """
    try:
        rules = get_key_rules()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading configuration: {str(e)}")
