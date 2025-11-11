from fastapi import APIRouter, Depends
from .auth import get_current_user
from typing import Optional

router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)

@router.get("/")
async def get_stats():
    """
    Get overview statistics for the dashboard
    """
    return {
        "shadowIT": 12,  # placeholder
        "users": 156,    # placeholder
        "compliance": 85, # placeholder %
        "alerts": 3      # placeholder
    }