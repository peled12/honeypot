from fastapi import Request, HTTPException
from redis import Redis

# connect to redis
redis = Redis(host="redis", port=6379, decode_responses=True)

# rate limiting params
RATE_LIMIT = 100       # number of requests allowed
WINDOW_SIZE = 60       # time window in seconds

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    # increment counter for this ip
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, WINDOW_SIZE)

    if count > RATE_LIMIT:
        ttl = redis.ttl(key) # time to live for the key
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {ttl} seconds."
        )

    return await call_next(request)
