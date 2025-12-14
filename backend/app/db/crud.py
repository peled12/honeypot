from sqlalchemy.orm import Session
from app.db import models
from app.schemas import EventCreate
from app.redis.redis_publisher import publish_event
from app.utils.cryptography import decrypt_data, encrypt_data

def create_event(db: Session, event_in: EventCreate):
    # convert to dict and encrypt all fields
    data = event_in.model_dump(exclude_unset=True)  # only fields provided
    encrypted_data = encrypt_data(data)

    event = models.Event(**encrypted_data) # create the event instance
    db.add(event)
    db.commit()
    db.refresh(event)

    # publish to redis
    publish_event(event.to_dict())

    return event

def get_all_events(db: Session):
    events = db.query(models.Event).all()

    # convert each object to dict and decrypt each
    decrypted_events = [decrypt_data(event.to_dict()) for event in events]
    return decrypted_events


