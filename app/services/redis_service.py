import redis.asyncio as redis
import json
from datetime import datetime
from app.config import REDIS_HOST, REDIS_PORT, REDIS_USERNAME, REDIS_PASSWORD
# Initialize Redis connection
# redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
    db=0,
)

 

# Custom JSON encoder to handle datetime objects
def custom_json_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO format string
    raise TypeError(f"Type {type(obj)} not serializable")

# Custom JSON decoder to handle datetime strings
def custom_json_decoder(obj):
    for key, value in obj.items():
        if isinstance(value, str):
            try:
                # Try to parse datetime strings
                obj[key] = datetime.fromisoformat(value)
            except ValueError:
                pass  # Leave value as string if it's not a valid datetime string
    return obj

async def save_to_redis(key: str, value: object):
    """Set data to Redis, converting datetime to ISO format strings if needed."""
    try:
        serialized_value = json.dumps(value, default=custom_json_encoder)
        await redis_client.set(key, serialized_value)
    except Exception as e:
        print(f"Error saving to Redis: {e}")

async def get_from_redis(key: str) -> object:
    """Get data from Redis, converting ISO format strings back to datetime if needed."""
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data, object_hook=custom_json_decoder)
        return None
    except Exception as e:
        print(f"Error retrieving from Redis: {e}")
        return None
