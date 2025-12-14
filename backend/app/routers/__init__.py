# from .auth_router import router as auth_router
from .health_router import router as health_router
from .testing_router import router as testing_router
from .summary_router import router as summary_router

# dont include the honeypot router as it will be imported separately in main_honeypot.py

__all__ = ["health_router", "testing_router", "summary_router"]