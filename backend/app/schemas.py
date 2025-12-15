# app/schemas.py
from datetime import datetime, timezone
import hashlib
from fastapi import Request
from pydantic import BaseModel
from typing import Optional

from app.utils.constants import UNKNOWN, SERVICES
from app.utils.geoip import get_country_from_ip

class EventCreate(BaseModel):
    src_ip: str
    src_port: Optional[int] = None
    dest_port: Optional[int] = None
    service: Optional[str] = None
    action: Optional[str] = None
    banner: Optional[str] = None
    raw_payload: Optional[str] = None
    payload_len: Optional[int] = None
    full_path: Optional[str] = None
    flagged: Optional[bool] = False
    reputation_score: Optional[float] = None
    geo_country: Optional[str] = None
    fingerprint: Optional[str] = None
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

    @classmethod
    async def from_http(cls, full_path: str, request: Request, banner: str = None, notes: list[str] = None):
        """Create EventCreate from HTTP request data"""
        client = request.client
        src_ip = client.host if client else UNKNOWN
        src_port = getattr(client, "port", None)
        dest_port = request.url.port or 80

        headers = dict(request.headers)
        user_agent = headers.get("user-agent", UNKNOWN)
        method = request.method

        # parse payload
        try:
            raw_bytes = await request.body()
            raw_payload = raw_bytes.decode(errors="ignore") if raw_bytes else None
        except Exception:
            raw_payload = None

        fingerprint_data = f"{src_ip}{user_agent}{method}{full_path}"
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()

        timestamp = datetime.now(timezone.utc)

        geo_country = await get_country_from_ip(src_ip)

        return cls(
            src_ip=src_ip,
            src_port=src_port,
            dest_port=dest_port,
            service=SERVICES.HTTP,
            action=method,
            banner=banner,
            raw_payload=raw_payload,
            full_path=full_path,
            geo_country=geo_country,
            fingerprint=fingerprint,
            notes=cls.analize_notes(user_agent, raw_payload, SERVICES.HTTP, banner, method, notes),
            timestamp=timestamp
        )
    
    @classmethod
    async def from_ssh(
        cls,
        src_ip: str,
        src_port: Optional[int],
        dest_port: int = 2222,
        command: Optional[str] = None,
        banner: Optional[str] = None,
        full_path: Optional[str] = None,
        notes: list[str] = None
    ):
        """Create EventCreate from SSH session data"""
        raw_payload = command or None
        service = SERVICES.SSH

        fingerprint_data = f"{src_ip}{command or ''}{full_path or ''}"
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()
        method = "SSH_COMMAND"

        timestamp = datetime.now(timezone.utc)
        geo_country = await get_country_from_ip(src_ip)

        return cls(
            src_ip=src_ip,
            src_port=src_port,
            dest_port=dest_port,
            service=service,
            action=method,
            banner=banner,
            raw_payload=raw_payload,
            full_path=full_path,
            geo_country=geo_country,
            fingerprint=fingerprint,
            notes=cls.analize_notes(None, raw_payload, service, banner, method, notes),
            timestamp=timestamp
        )
    
    @classmethod
    async def from_ftp(
        cls,
        src_ip: str,
        src_port: int | None,
        dest_port: int,
        full_path: str | None,
        raw_bytes: bytes | None,
        command: str,
        banner: str | None = None,
        notes: list[str] | None = None
    ):
        """Create EventCreate from FTP interaction"""
        from datetime import datetime, timezone
        import hashlib

        # decode raw bytes to string
        try:
            raw_payload = raw_bytes.decode(errors="ignore") if raw_bytes else None
        except Exception:
            raw_payload = None

        payload_len = len(raw_bytes) if raw_bytes else 0

        method = "FTP_COMMAND"
        service = SERVICES.FTP

        # get fingerprint
        fingerprint_data = f"{src_ip}{full_path or ''}{payload_len}{command}"
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()

        timestamp = datetime.now(timezone.utc)
        geo_country = await get_country_from_ip(src_ip)

        return cls(
            src_ip=src_ip,
            src_port=src_port,
            dest_port=dest_port,
            service=service,
            action=command,
            banner=banner,
            raw_payload=raw_payload,
            full_path=full_path,
            geo_country=geo_country,
            fingerprint=fingerprint,
            notes=cls.analize_notes(None, raw_payload, service, banner, method, notes),
            timestamp=timestamp
        )

    
    @staticmethod
    def analize_notes(user_agent, raw_payload, service, banner, method, existing_notes=None):
        notes = []

        # missing User-Agent header (may indicate non-browser tools or bots)
        if user_agent == UNKNOWN:
            notes.append("missing user-agent header")
        elif user_agent != None:
            notes.append(f"UA: {user_agent}") # add user agent to notes if its a normal http request

        # suspicious js code in payload (possible XSS attempt)
        if raw_payload and "<script>" in raw_payload.lower():
            notes.append("possible XSS payload")

        if service == SERVICES.SSH and SERVICES.SSH not in (banner or "").lower():
            notes.append("ssh port but no ssh banner detected")

        # path traversal attempt
        if raw_payload and "../" in raw_payload:
            notes.append("path traversal attempt")

        # empty post request
        if method == "POST" and not raw_payload:
            notes.append("empty POST request")

        # merge with any extra notes passed in
        if existing_notes:
            notes.extend(existing_notes)

        # join all notes into a single string (or None if no notes)
        return "; ".join(notes) if notes else None
