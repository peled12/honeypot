from fastapi import APIRouter
import time
import socket

router = APIRouter(prefix="/health", tags=["Health"])

# returns basic health info
@router.get("/", summary="Check API health")
def health_check():
    return {
        "status": "ok",
        "service": "honeypot-api",
        "hostname": socket.gethostname(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
