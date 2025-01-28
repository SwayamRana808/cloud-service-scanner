from fastapi import APIRouter,Request
from app.services.aws_services import get_iam_users
from app.security.iam_security_check import iam_security_check
from app.services.redis_service import save_to_redis, get_from_redis
from app.services.websocket_service import update_service_data

router = APIRouter()

@router.get("/getiam")
async def scan_iam(request: Request = None, full_check: bool = False):
    """
    API endpoint to scan all IAM users for security issues.
    If no IAM users are found, return an empty response.
    """
    # Check for the 'full_check' header to decide if a full check is required
    if request:
        full_check = request.headers.get("X-Full-Check", "false").lower() == "true"

    if not full_check:
        # Try to fetch IAM data from Redis first
        iam_data = await get_from_redis("iam_data")
        if iam_data:
            return {"users": iam_data}

    # If no data in Redis or full check is requested, perform a full scan

    users = get_iam_users()
    
    if not users:
        # Return an empty response instead of raising an error
        return {"users": []}

    # Run the security checks
    checked_users = iam_security_check(users)
    await save_to_redis("iam_data", checked_users)
    await update_service_data("iam")
    return {"users": checked_users}
