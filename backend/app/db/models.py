from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, func
from .database import Base

class Event(Base):
    # model that stores attack events
    __tablename__ = "events"

    # all strings because data in the db would be encrypted
    id = Column(Integer, primary_key=True, index=True)   # unique ID
    timestamp = Column(String, nullable=False)

    src_ip = Column(String, index=True, nullable=False)
    src_port = Column(String(16), nullable=True)
    dest_port = Column(String(16), nullable=True)
    service = Column(String(32), nullable=True)

    action = Column(String(128), nullable=True, index=True)
    banner = Column(String(512), nullable=True)
    raw_payload = Column(Text, nullable=True)
    full_path = Column(String(512), nullable=True, index=True)

    geo_country = Column(String(2), nullable=True) # 2 letter country code
    fingerprint = Column(String(128), nullable=True)
    notes = Column(String(512), nullable=True)

    # helper to convert to dict
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Original model with correct types:
    # id = Column(Integer, primary_key=True, index=True)   # unique ID
    # timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # src_ip = Column(String, index=True, nullable=False)
    # src_port = Column(Integer, nullable=True)
    # dest_port = Column(Integer, nullable=True)
    # service = Column(String(32), nullable=True)

    # action = Column(String(128), nullable=True, index=True)
    # banner = Column(String(512), nullable=True)
    # raw_payload = Column(Text, nullable=True)
    # full_path = Column(String(512), nullable=True, index=True)

    # geo_country = Column(String(2), nullable=True) # 2 letter country code
    # fingerprint = Column(String(128), nullable=True)
    # notes = Column(String(512), nullable=True)