from datetime import datetime
import json
import asyncio
from app.redis_client import redis_client
from app.sockets.sockets import emit_new_event
from app.utils.cryptography import decrypt_data

# listen to redis channel and emit events
async def start_redis_listener(channel: str = "events"):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    print(f"[Redis] Subscribed to channel '{channel}'")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message:
            try:
                # get the data
                encrypted_data = json.loads(message["data"])
                data = decrypt_data(encrypted_data) # decrypt it while restoring original data types 

                # convert timestamp back to datetime safely
                timestamp = data.get("timestamp")
                if isinstance(timestamp, str):
                    try:
                        data["timestamp"] = datetime.fromisoformat(timestamp)
                    except ValueError:
                        pass

                await emit_new_event(data)
            except Exception as e:
                print(f"[RedisListener] Failed to process message: {e}")
        await asyncio.sleep(0.01)
