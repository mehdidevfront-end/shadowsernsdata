from fastapi import APIRouter, Depends
from .auth import get_current_user

router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)

@router.get("/")
async def get_stats(current_user = Depends(get_current_user)):
    """
    Get overview statistics for the dashboard
    """
    return {
        "shadowIT": 12,  # placeholder
        "users": 156,    # placeholder
        "compliance": 85, # placeholder %
        "alerts": 3      # placeholder
    }