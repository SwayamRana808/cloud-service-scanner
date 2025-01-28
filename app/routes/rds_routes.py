from fastapi import APIRouter, Request
from app.services.aws_services import get_rds_instances
from app.security.rds_security_check import rds_security_check
from app.services.redis_service import save_to_redis, get_from_redis
from app.services.websocket_service import update_service_data
router = APIRouter()

@router.get("/getrds")
async def scan_rds(request: Request = None, full_check: bool = False):
    """
    API endpoint to scan all RDS instances for security issues.
    """
    if request:
        full_check = request.headers.get("X-Full-Check", "false").lower() == "true"

    if not full_check:
        # Try to fetch RDS data from Redis
        rds_data = await get_from_redis("rds_data")
        if rds_data:
            return {"instances": rds_data}
        
    instances_by_region = get_rds_instances()

    if not instances_by_region:
        # Return an empty response instead of raising an error
        return {"instances": []}

    # Run the security checks
    checked_instances = rds_security_check(instances_by_region)
    await save_to_redis("rds_data", checked_instances)
    await update_service_data("rds")

    return {"instances": checked_instances}
