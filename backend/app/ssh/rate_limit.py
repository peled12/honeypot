import os

from app.redis_client import redis_client

SSH_RATE_LIMIT = int(os.getenv("SSH_RATE_LIMIT", "20"))
SSH_WINDOW = int(os.getenv("SSH_WINDOW", "60"))

# check if a given ip has exceeded rate limit
def check_ssh_rate_limit(ip: str) -> bool:
    if not ip:
        return True # allow unknown ips for testing
    key = f"rate_limit:ssh:{ip}"
    try:
        count = redis_client.incr(key)
        if count == 1:
            redis_client.expire(key, SSH_WINDOW) # set expiration on first increment
        return count <= SSH_RATE_LIMIT
    except Exception as e:
        print(f"[ssh.rate_limit] redis error: {e}")
        return True
