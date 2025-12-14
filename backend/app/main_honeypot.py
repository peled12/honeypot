import json
from fastapi import FastAPI, Request, Response, status

from .utils.rate_limiter import rate_limit_middleware
from .routers.honeypot_router import router as honeypot_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv() # load environment variables
frontend_origins = os.getenv("FRONTEND_ORIGINS", "").split(",")

app = FastAPI(title="Honeypot Trap", docs_url=None, redoc_url=None)

# allow all origins to access the honeypot endpoints (except blocked ones)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # allow all browsers/tools to reach it
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,       # no credentials needed
)

# origins to block
BLOCKED_ORIGINS = {origin.strip() for origin in frontend_origins if origin.strip()} # strip spaces and ignore empty

# middleware to block requests from frontend origins
@app.middleware("http")
async def block_known_frontends(request: Request, call_next):
    origin = request.headers.get("origin")
    if origin and origin in BLOCKED_ORIGINS:
        # return 403 to browser clients from your frontend
        return Response(
            content=json.dumps({"detail": "Forbidden"}),
            status_code=status.HTTP_403_FORBIDDEN,
            media_type="application/json",
        )
    # otherwise allow request to proceed
    return await call_next(request)

# apply rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# include only the bait endpoints
app.include_router(honeypot_router)