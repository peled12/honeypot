import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

FRONTEND_ORIGINS = [o.strip() for o in os.getenv("FRONTEND_ORIGINS", "").split(",") if o.strip()] # get the list of the allowed origins

# user for encrypting / decrypting database fields
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")

# list of the allowed ip's
ALLOWED_IPS = os.getenv("ALLOWED_IPS", "").split(",")

# helper to check if an ip is allowed
def is_ip_allowed(ip: str) -> bool:
    return ip in ALLOWED_IPS
