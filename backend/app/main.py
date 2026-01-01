import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.routers import *
from .redis.redis_listener import start_redis_listener
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.utils.config import FRONTEND_ORIGINS, is_ip_allowed
from .sockets.sockets import init_sockets

# TODO: fix socket in frontend
# TODO: deploy my server
# TODO: ensure implementation of rate limiting

load_dotenv() # load environment variables

# define lifespan for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    listener_task = asyncio.create_task(start_redis_listener())
    print("Redis listener started")
    
    yield

    # shut down logic
    listener_task.cancel()
    print("Redis listener stopped")

# start the fastapi app
app = FastAPI(title="Honeypot Backend", lifespan=lifespan)
socket_manager = init_sockets(app) # init socket

# add cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS, # strip spaces and ignore empty
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# catch SQLAlchemy errors globally
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Database error: {str(exc)}"},
    )

# catch anything else
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# middleware for checking if the requesting ip is allowed
@app.middleware("http")
async def ip_whitelist_middleware(request: Request, call_next):
    client_ip = request.client.host
    print("Incoming IP:", client_ip)
    
    if not is_ip_allowed(client_ip):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="IP not allowed")
    response = await call_next(request)
    return response

# middleware for logging requests and catching unhandled exceptions
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"Unhandled error on {request.url}: {e}")
        raise  # let global handler catch it

# Include routers
app.include_router(testing_router)
app.include_router(summary_router)
app.include_router(health_router)