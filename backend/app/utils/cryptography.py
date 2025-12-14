# app/utils/encryption.py
from cryptography.fernet import Fernet
from app.utils.config import BACKEND_API_KEY as ENCRYPTION_KEY
from datetime import datetime

fernet = Fernet(ENCRYPTION_KEY.encode())

# define the fields that should be encrypted
ENCRYPTING_FIELDS = [
    "src_ip", "src_port", "dest_port", "service",
    "action", "banner", "raw_payload", "full_path",
    "flagged", "reputation_score", "payload_len",
    "geo_country", "fingerprint", "notes", "timestamp"
]

def encrypt_field(value):
    """Encrypt a single value, converting to string first if needed."""
    if value is None:
        return None
    
    return fernet.encrypt(str(value).encode()).decode()

def decrypt_field(value, original_type=str):
    """Decrypt a single value and cast back to the original type."""
    if value is None:
        return None
    
    decrypted = fernet.decrypt(value.encode()).decode()

    # convert back to the original type
    if original_type == int:
        return int(decrypted)
    if original_type == bool:
        return decrypted.lower() in ("true", "1")
    if original_type == float:
        return float(decrypted)
    if original_type == datetime:
        return datetime.fromisoformat(decrypted)
    return decrypted

def encrypt_data(obj: dict) -> dict:
    """Encrypt all fields in a dict according to ENCRYPTING_FIELDS."""
    for field in ENCRYPTING_FIELDS:
        if field in obj:
            obj[field] = encrypt_field(obj[field])
            
    return obj

def decrypt_data(obj: dict) -> dict:
    """Decrypt all fields in a dict according to ENCRYPTED_FIELDS."""
    # field types to restore
    FIELD_TYPES = {
        "src_port": int,
        "dest_port": int,
        "flagged": bool,
        "reputation_score": int,
        "payload_len": int,
        "timestamp": datetime
    }
    
    for field in ENCRYPTING_FIELDS:
        if field in obj:
            obj[field] = decrypt_field(obj[field], FIELD_TYPES.get(field, str))
    return obj
