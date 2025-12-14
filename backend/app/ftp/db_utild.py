from app.schemas import EventCreate
import asyncio
from app.db import crud
from app.db.database import SessionLocal

def save_event_sync(event_obj):
    db = SessionLocal()  # create a new independent DB session
    try:
        crud.create_event(db, event_obj) # commit and publish to redis (internally called model_dump)
    except Exception as e:
        print(f"[ftp] DB save error: {e}")
    finally:
        db.close() # close the db session

# saves event in background without blocking main flow
async def save_event_background(event_obj: EventCreate):
    loop = asyncio.get_running_loop()
    # run the blocking save in a background thread without blocking main flow
    await loop.run_in_executor(None, save_event_sync, event_obj)
