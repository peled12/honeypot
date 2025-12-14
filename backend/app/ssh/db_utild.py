from app.db import crud
from app.db.database import SessionLocal

# synchronous helper to save event to db
def save_event_sync(event_obj):
    db = SessionLocal()  # create a new independent DB session
    try:
        crud.create_event(db, event_obj) # commit and publish to redis (internally called model_dump)
    except Exception as e:
        print(f"[ssh.auth] DB save error: {e}")
    finally:
        db.close() # close the db session
