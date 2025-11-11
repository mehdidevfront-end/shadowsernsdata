from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
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
    },
    {
        "id": "log2",
        "timestamp": "2025-11-07T09:15:00",
        "service": "drive",
        "action": "upload",
        "user": "sarah@company.com",
        "resource_id": "file456",
        "resource_name": "Q4_Budget.xlsx",
        "details": {"size": "2.5MB", "folder": "Finance"},
        "status": "success"
    },
    {
        "id": "log3",
        "timestamp": "2025-11-07T08:45:00",
        "service": "docs",
        "action": "edit",
        "user": "mike@company.com",
        "resource_id": "doc789",
        "resource_name": "Project Plan",
        "details": {"changes": 23, "collaborators": ["john@company.com"]},
        "status": "success"
    },
    {
        "id": "log4",
        "timestamp": "2025-11-06T16:20:00",
        "service": "sheets",
        "action": "share",
        "user": "admin@company.com",
        "resource_id": "sheet321",
        "resource_name": "Employee Data",
        "details": {"shared_with": ["hr@company.com"], "permission": "edit"},
        "status": "success"
    },
    {
        "id": "log5",
        "timestamp": "2025-11-06T14:10:00",
        "service": "meet",
        "action": "join",
        "user": "team@company.com",
        "resource_id": "meet987",
        "resource_name": "Daily Standup",
        "details": {"duration": "25min", "participants": 8},
        "status": "success"
    },
    {
        "id": "log6",
        "timestamp": "2025-11-06T11:00:00",
        "service": "email",
        "action": "receive",
        "user": "john@company.com",
        "resource_id": "msg456",
        "resource_name": "Security Alert",
        "details": {"from": "security@company.com", "attachments": 0},
        "status": "success"
    },
    {
        "id": "log7",
        "timestamp": "2025-11-05T15:30:00",
        "service": "drive",
        "action": "delete",
        "user": "sarah@company.com",
        "resource_id": "file999",
        "resource_name": "Old_Draft.docx",
        "details": {"size": "500kb", "recovery_until": "2025-11-19"},
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
    limit: int = Query(default=100, le=1000)
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
    
    return filtered_logs[:limit]

@router.get("/{service}/stats")
async def get_service_stats(
    service: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
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
        "service": service,
        "total_events": len(filtered_logs),
        "success_count": success_count,
        "error_count": error_count,
        "success_rate": (success_count / len(filtered_logs) * 100) if filtered_logs else 0,
        "most_active_users": list(set([log["user"] for log in filtered_logs[:5]]))
    }

@router.get("/email/stats")
async def get_email_stats(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Statistiques spécifiques aux emails
    """
    email_logs = [log for log in mock_logs if log["service"] == "email"]
    
    return {
        "total_sent": len([log for log in email_logs if log["action"] == "send"]),
        "total_received": len([log for log in email_logs if log["action"] == "receive"]),
        "total_events": len(email_logs),
        "average_size": "2.5MB",
        "top_senders": ["john@company.com", "security@company.com"],
        "success_rate": 98.5
    }

@router.get("/drive/stats")
async def get_drive_stats():
    """
    Statistiques spécifiques à Google Drive
    """
    drive_logs = [log for log in mock_logs if log["service"] == "drive"]
    return {
        "total_storage": "15GB",
        "used_storage": "8.5GB",
        "file_count": 1250,
        "shared_files": 320,
        "recent_activities": len(drive_logs),
        "uploads": len([log for log in drive_logs if log["action"] == "upload"]),
        "downloads": len([log for log in drive_logs if log["action"] == "download"]),
        "deletes": len([log for log in drive_logs if log["action"] == "delete"])
    }

@router.get("/docs/stats")
async def get_docs_stats():
    """
    Statistiques spécifiques à Google Docs
    """
    docs_logs = [log for log in mock_logs if log["service"] == "docs"]
    return {
        "active_documents": 85,
        "shared_documents": 42,
        "recent_edits": len(docs_logs),
        "collaborators": 8,
        "total_events": len(docs_logs)
    }

@router.get("/sheets/stats")
async def get_sheets_stats():
    """
    Statistiques spécifiques à Google Sheets
    """
    sheets_logs = [log for log in mock_logs if log["service"] == "sheets"]
    return {
        "active_sheets": 32,
        "shared_sheets": 18,
        "data_size": "1.2GB",
        "formulas_count": 1500,
        "recent_events": len(sheets_logs),
        "total_events": len(sheets_logs)
    }

@router.get("/meet/stats")
async def get_meet_stats():
    """
    Statistiques spécifiques à Google Meet
    """
    meet_logs = [log for log in mock_logs if log["service"] == "meet"]
    return {
        "total_meetings": 145,
        "active_meetings": 3,
        "total_participants": 289,
        "average_duration": "32min",
        "recent_meetings": len(meet_logs),
        "total_events": len(meet_logs)
    }