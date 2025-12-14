# routes here are used for the main app, not for bait

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import crud, models
from app.schemas import EventCreate
from ..deps import get_db

router = APIRouter(prefix="/testing", tags=["Testing"])

# POST endpoint
@router.post("/add-event", status_code=201)
def create_event_endpoint(event: EventCreate, db: Session = Depends(get_db)):
    try:
        db_event = crud.create_event(db, event)
        return {"id": db_event.id, "timestamp": db_event.timestamp}
    except Exception as e:
        db.rollback() # rollback if something went wrong
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create event: {str(e)}"
        )

# Get endpoint (all events)
@router.get("/get-events", status_code=200)
def get_all_events(db: Session = Depends(get_db)):
    try:
        events = crud.get_all_events(db) # get all the events

        return events
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch events: {str(e)}"
        )