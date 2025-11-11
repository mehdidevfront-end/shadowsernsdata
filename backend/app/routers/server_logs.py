from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import random

router = APIRouter(
    prefix="/server-logs",
    tags=["server-logs"]
)

class ServerLogEntry(BaseModel):
    id: str
    timestamp: datetime
    server_name: str
    log_type: str  # 'cpu', 'memory', 'disk', 'network', 'system'
    level: str  # 'info', 'warning', 'error', 'critical'
    message: str
    details: dict
    value: Optional[float] = None

class WiFiLogEntry(BaseModel):
    id: str
    timestamp: datetime
    event_type: str  # 'connect', 'disconnect', 'auth_failure', 'signal_low'
    device_name: str
    device_mac: str
    device_ip: Optional[str] = None
    ssid: str
    signal_strength: Optional[int] = None
    details: dict

# Mock data pour les logs serveur
server_logs = [
    {
        "id": "srv1",
        "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
        "server_name": "web-server-01",
        "log_type": "cpu",
        "level": "warning",
        "message": "High CPU usage detected",
        "details": {"cores": 8, "usage_per_core": [85, 92, 78, 88, 95, 82, 90, 87]},
        "value": 87.5
    },
    {
        "id": "srv2",
        "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(),
        "server_name": "db-server-01",
        "log_type": "memory",
        "level": "error",
        "message": "Memory usage critical",
        "details": {"total_gb": 32, "used_gb": 30.5, "available_gb": 1.5},
        "value": 95.3
    },
    {
        "id": "srv3",
        "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
        "server_name": "app-server-02",
        "log_type": "disk",
        "level": "warning",
        "message": "Disk space running low",
        "details": {"partition": "/dev/sda1", "total_gb": 500, "used_gb": 425, "available_gb": 75},
        "value": 85.0
    },
    {
        "id": "srv4",
        "timestamp": (datetime.now() - timedelta(minutes=20)).isoformat(),
        "server_name": "web-server-01",
        "log_type": "network",
        "level": "info",
        "message": "High network traffic",
        "details": {"inbound_mbps": 850, "outbound_mbps": 420, "connections": 1250},
        "value": 850
    },
    {
        "id": "srv5",
        "timestamp": (datetime.now() - timedelta(minutes=25)).isoformat(),
        "server_name": "backup-server",
        "log_type": "system",
        "level": "info",
        "message": "Backup completed successfully",
        "details": {"backup_size_gb": 125, "duration_minutes": 45, "files_count": 15890},
        "value": 125
    },
    {
        "id": "srv6",
        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
        "server_name": "db-server-01",
        "log_type": "system",
        "level": "critical",
        "message": "Database connection pool exhausted",
        "details": {"max_connections": 100, "active_connections": 100, "waiting_queries": 45},
        "value": 100
    },
    {
        "id": "srv7",
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "server_name": "app-server-01",
        "log_type": "cpu",
        "level": "info",
        "message": "CPU usage normal",
        "details": {"cores": 4, "average_usage": 45},
        "value": 45.0
    }
]

# Mock data pour les logs WiFi
wifi_logs = [
    {
        "id": "wifi1",
        "timestamp": (datetime.now() - timedelta(minutes=2)).isoformat(),
        "event_type": "connect",
        "device_name": "iPhone-John",
        "device_mac": "A4:83:E7:2B:5C:1D",
        "device_ip": "192.168.1.105",
        "ssid": "Company-WiFi-5G",
        "signal_strength": -45,
        "details": {"auth_method": "WPA2-Enterprise", "channel": 149, "bandwidth": "80MHz"}
    },
    {
        "id": "wifi2",
        "timestamp": (datetime.now() - timedelta(minutes=8)).isoformat(),
        "event_type": "disconnect",
        "device_name": "MacBook-Sarah",
        "device_mac": "88:66:5A:1C:3F:42",
        "device_ip": "192.168.1.78",
        "ssid": "Company-WiFi",
        "signal_strength": -65,
        "details": {"reason": "client_disconnect", "duration_minutes": 125}
    },
    {
        "id": "wifi3",
        "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
        "event_type": "auth_failure",
        "device_name": "Unknown-Device",
        "device_mac": "00:11:22:33:44:55",
        "device_ip": None,
        "ssid": "Company-WiFi",
        "signal_strength": -52,
        "details": {"reason": "invalid_password", "attempts": 3}
    },
    {
        "id": "wifi4",
        "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
        "event_type": "signal_low",
        "device_name": "Laptop-Mike",
        "device_mac": "C8:D7:B1:4E:8A:9C",
        "device_ip": "192.168.1.142",
        "ssid": "Company-WiFi-2G",
        "signal_strength": -78,
        "details": {"previous_signal": -62, "location": "Conference Room B"}
    },
    {
        "id": "wifi5",
        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
        "event_type": "connect",
        "device_name": "iPad-Admin",
        "device_mac": "F4:0F:24:3B:7D:8E",
        "device_ip": "192.168.1.201",
        "ssid": "Company-WiFi-5G",
        "signal_strength": -38,
        "details": {"auth_method": "WPA2-PSK", "channel": 36, "bandwidth": "80MHz"}
    },
    {
        "id": "wifi6",
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "event_type": "connect",
        "device_name": "Android-Team",
        "device_mac": "2C:54:91:88:C9:E3",
        "device_ip": "192.168.1.156",
        "ssid": "Company-WiFi",
        "signal_strength": -55,
        "details": {"auth_method": "WPA2-Enterprise", "channel": 6, "bandwidth": "40MHz"}
    }
]

@router.get("/server", response_model=List[ServerLogEntry])
async def get_server_logs(
    server_name: Optional[str] = None,
    log_type: Optional[str] = None,
    level: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(default=100, le=1000)
):
    """
    Récupérer les logs du serveur local avec filtres
    """
    filtered_logs = server_logs
    
    if server_name:
        filtered_logs = [log for log in filtered_logs if log["server_name"] == server_name]
    if log_type:
        filtered_logs = [log for log in filtered_logs if log["log_type"] == log_type]
    if level:
        filtered_logs = [log for log in filtered_logs if log["level"] == level]
    if start_date:
        start = datetime.fromisoformat(start_date)
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) >= start]
    if end_date:
        end = datetime.fromisoformat(end_date)
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) <= end]
    
    return filtered_logs[:limit]

@router.get("/server/stats")
async def get_server_stats():
    """
    Statistiques globales des serveurs
    """
    total_logs = len(server_logs)
    critical_count = len([log for log in server_logs if log["level"] == "critical"])
    error_count = len([log for log in server_logs if log["level"] == "error"])
    warning_count = len([log for log in server_logs if log["level"] == "warning"])
    
    servers = list(set([log["server_name"] for log in server_logs]))
    
    return {
        "total_servers": len(servers),
        "total_logs": total_logs,
        "critical_alerts": critical_count,
        "errors": error_count,
        "warnings": warning_count,
        "info": total_logs - critical_count - error_count - warning_count,
        "servers": servers,
        "average_cpu": 66.25,
        "average_memory": 72.5,
        "average_disk": 68.0
    }

@router.get("/wifi", response_model=List[WiFiLogEntry])
async def get_wifi_logs(
    event_type: Optional[str] = None,
    device_name: Optional[str] = None,
    ssid: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(default=100, le=1000)
):
    """
    Récupérer les logs WiFi avec filtres
    """
    filtered_logs = wifi_logs
    
    if event_type:
        filtered_logs = [log for log in filtered_logs if log["event_type"] == event_type]
    if device_name:
        filtered_logs = [log for log in filtered_logs if device_name.lower() in log["device_name"].lower()]
    if ssid:
        filtered_logs = [log for log in filtered_logs if log["ssid"] == ssid]
    if start_date:
        start = datetime.fromisoformat(start_date)
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) >= start]
    if end_date:
        end = datetime.fromisoformat(end_date)
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]) <= end]
    
    return filtered_logs[:limit]

@router.get("/wifi/stats")
async def get_wifi_stats():
    """
    Statistiques WiFi
    """
    total_logs = len(wifi_logs)
    connections = len([log for log in wifi_logs if log["event_type"] == "connect"])
    disconnections = len([log for log in wifi_logs if log["event_type"] == "disconnect"])
    auth_failures = len([log for log in wifi_logs if log["event_type"] == "auth_failure"])
    
    devices = list(set([log["device_name"] for log in wifi_logs]))
    ssids = list(set([log["ssid"] for log in wifi_logs]))
    
    return {
        "total_events": total_logs,
        "connections": connections,
        "disconnections": disconnections,
        "auth_failures": auth_failures,
        "signal_issues": len([log for log in wifi_logs if log["event_type"] == "signal_low"]),
        "active_devices": len(devices),
        "available_ssids": len(ssids),
        "devices": devices[:10],
        "ssids": ssids,
        "average_signal": -54
    }

@router.get("/server/{server_name}/metrics")
async def get_server_metrics(server_name: str):
    """
    Métriques détaillées pour un serveur spécifique
    """
    server_specific_logs = [log for log in server_logs if log["server_name"] == server_name]
    
    if not server_specific_logs:
        return {"error": "Server not found"}
    
    cpu_logs = [log for log in server_specific_logs if log["log_type"] == "cpu"]
    memory_logs = [log for log in server_specific_logs if log["log_type"] == "memory"]
    
    return {
        "server_name": server_name,
        "status": "online",
        "uptime_hours": 168,
        "cpu_usage": cpu_logs[0]["value"] if cpu_logs else 0,
        "memory_usage": memory_logs[0]["value"] if memory_logs else 0,
        "disk_usage": 68.5,
        "network_in_mbps": 245,
        "network_out_mbps": 180,
        "active_connections": 856,
        "total_logs": len(server_specific_logs)
    }
