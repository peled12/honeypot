import json
import os
from typing import Dict, Any
from app.redis_client import redis_client

# default publish channel
PUBLISH_CHANNEL = os.getenv("SSH_PUB_CHANNEL", "events")

# publish an event to redis
def publish_event(event: Dict[str, Any], channel: str = None) -> None:
    target_channel = channel or PUBLISH_CHANNEL

    # ensure timestamp exists
    if "timestamp" not in event:
        from datetime import datetime, timezone
        event["timestamp"] = datetime.now(timezone.utc).isoformat()

    try:
        redis_client.publish(target_channel, json.dumps(event))
    except Exception as e:
        print(f"[redis_publisher] Failed to publish event: {e}")
