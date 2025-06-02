from fastapi import APIRouter, HTTPException
from .config_services import ConfigServices

router = APIRouter(prefix="/config", tags=["config"])

services = ConfigServices()

@router.get("/config/categorization")
async def get_categorization_config():
    """
    Returns the categorization configuration.
    """
    try:
        rules = services.get_key_rules()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading configuration: {str(e)}")
