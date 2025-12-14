import random
from fastapi import APIRouter, Request, Depends, Response, status
from sqlalchemy.orm import Session
from app.deps import get_db
from app.db import crud, models
from app.schemas import EventCreate
from app.utils.banner_rotation import get_http_banner

router = APIRouter(tags=["Honeypot"])

IGNORE_EXACT = {
    "favicon.ico",
    "robots.txt",
    "apple-touch-icon.png",
    "apple-touch-icon-precomposed.png",
    "browserconfig.xml",
    "site.webmanifest",
}
IGNORE_PREFIXES = (
    ".well-known",
)

# catch-all route to log any access attempts to undefined paths
@router.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
)
async def honeypot_catch_all(full_path: str, request: Request, db: Session = Depends(get_db)):
    # normalize path
    normalized_path = full_path.strip("/")
    
    # select a random banner
    banner = get_http_banner(request.client.host) # get banner based on ip rotation

    # initialize a generic response
    generic_404_response = Response(
        content = "Resource not found.",
        status_code = status.HTTP_404_NOT_FOUND,
        headers={"Server": banner}
    )

    # ignore certain paths
    if normalized_path in IGNORE_EXACT or normalized_path.startswith(IGNORE_PREFIXES):
        print(f"[HONEYPOT IGNORED] {request.client} requested {full_path}")
        return generic_404_response # return a generic response
    
    # get the request details
    event_data = await EventCreate.from_http(full_path, request, banner)

    # save to db
    crud.create_event(db, event_data)

    # return a generic response
    return generic_404_response
