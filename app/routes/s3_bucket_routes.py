from fastapi import APIRouter, Request
from app.services.aws_services import get_s3_buckets
from app.security.s3_security_check import s3_security_check
from app.services.redis_service import save_to_redis, get_from_redis
from app.services.websocket_service import update_service_data

router = APIRouter()

@router.get("/gets3")
async def scan_s3(request: Request = None, full_check: bool = False):
    """
    API endpoint to scan all S3 buckets for security issues.
    """
    if request:
        full_check = request.headers.get("X-Full-Check", "false").lower() == "true"

    if not full_check:
        # Try to fetch S3 data from Redis
        s3_data = await get_from_redis("s3_data")
        if s3_data:
            return {"buckets": s3_data}

    buckets = get_s3_buckets()

    if not buckets:
         return {"buckets": []}

    checked_buckets = s3_security_check(buckets)
    
    await save_to_redis("s3_data",checked_buckets)
    await update_service_data("s3")
    return {"buckets": checked_buckets}

