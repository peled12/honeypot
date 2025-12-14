import os

from app.redis_client import redis_client

FTP_RATE_LIMIT = int(os.getenv("FTP_RATE_LIMIT", "20"))
FTP_WINDOW = int(os.getenv("FTP_WINDOW", "60"))

# check if an ip exeeded the ftp rate limit
def check_ftp_rate_limit(ip: str) -> bool:
    if not ip:
        return True  # allow unknown ips for testing

    key = f"rate_limit:ftp:{ip}"

    try:
        count = redis_client.incr(key)

        if count == 1:
            redis_client.expire(key, FTP_WINDOW) # set expiration on first increment

        return count <= FTP_RATE_LIMIT

    except Exception as e:
        print(f"[ftp.rate_limit] Redis error: {e}")
        return True
