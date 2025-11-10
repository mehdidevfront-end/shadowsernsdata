from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from ..routers.auth import get_current_user

router = APIRouter(
    prefix="/google-logs",
    tags=["google-logs"]
)

class GoogleLogEntry(BaseModel):
    id: str
    timestamp: datetime
    service: str  # 'email', 'drive', 'docs', 'sheets'
    action: str
    user: str
    resource_id: str
    resource_name: str
    details: dict
    status: str

# Simulated data - replace with actual database
mock_logs = [
    {
        "id": "log1",
        "timestamp": "2025-11-07T10:30:00",
        "service": "email",
        "action": "send",
        "user": "john@company.com",
        "resource_id": "msg123",
        "resource_name": "Weekly Report",
        "details": {"recipients": ["team@company.com"], "size": "250kb"},
        "status": "success"
    }
]

@router.get("/", response_model=List[GoogleLogEntry])
async def get_logs(
    service: Optional[str] = None,
    user: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """
    Récupérer les logs filtrés par service, utilisateur, période et statut
    """
    filtered_logs = mock_logs
    
    if service:
        filtered_logs = [log for log in filtered_logs if log["service"] == service]
    if user:
        filtered_logs = [log for log in filtered_logs if log["user"] == user]
    if status:
        filtered_logs = [log for log in filtered_logs if log["status"] == status]
    if start_date:
        start = datetime.fromisoformat(start_date)
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) >= start]
    if end_date:
        end = datetime.fromisoformat(end_date)
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) <= end]
    
    return filtered_logs

@router.get("/{service}/stats")
async def get_service_stats(
    service: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """
    Obtenir des statistiques pour un service spécifique
    """
    filtered_logs = [log for log in mock_logs if log["service"] == service]
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) >= start]
    if end_date:
        end = datetime.fromisoformat(end_date)
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) <= end]
    
    success_count = len([log for log in filtered_logs if log["status"] == "success"])
    error_count = len([log for log in filtered_logs if log["status"] == "error"])
    
    return {
        "total_events": len(filtered_logs),
        "success_count": success_count,
        "error_count": error_count,
        "success_rate": success_count / len(filtered_logs) if filtered_logs else 0
    }

@router.get("/email/stats")
async def get_email_stats(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """
    Statistiques spécifiques aux emails
    """
    email_logs = [log for log in mock_logs if log["service"] == "email"]
    
    return {
        "total_sent": len([log for log in email_logs if log["action"] == "send"]),
        "total_received": len([log for log in email_logs if log["action"] == "receive"]),
        "average_size": "2.5MB",  # Placeholder
        "top_senders": ["user1@company.com", "user2@company.com"]
    }

@router.get("/drive/stats")
async def get_drive_stats(
    current_user = Depends(get_current_user)
):
    """
    Statistiques spécifiques à Google Drive
    """
    return {
        "total_storage": "15GB",
        "used_storage": "8.5GB",
        "file_count": 1250,
        "shared_files": 320,
        "recent_activities": 45
    }

@router.get("/docs/stats")
async def get_docs_stats(
    current_user = Depends(get_current_user)
):
    """
    Statistiques spécifiques à Google Docs
    """
    return {
        "active_documents": 85,
        "shared_documents": 42,
        "recent_edits": 15,
        "collaborators": 8
    }

@router.get("/sheets/stats")
async def get_sheets_stats(
    current_user = Depends(get_current_user)
):
    """
    Statistiques spécifiques à Google Sheets
    """
    return {
        "active_sheets": 32,
        "shared_sheets": 18,
        "data_size": "1.2GB",
        "formulas_count": 1500
    }