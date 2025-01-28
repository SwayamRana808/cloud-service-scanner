from fastapi import APIRouter, Request, HTTPException
from app.services.aws_services import get_ec2_instances
from app.security.ec2_security_check import ec2_security_check
from app.security.ec2_security_check import ec2_security_check
from app.services.redis_service import save_to_redis, get_from_redis
from app.services.websocket_service import update_service_data

import logging
router = APIRouter()
@router.get("/getec2")
async def scan_ec2_instances(request: Request = None, full_check: bool = False):
    """
    API endpoint to scan all EC2 instances for security group issues.
    """
    if request:
        full_check = request.headers.get("X-Full-Check", "false").lower() == "true"

    if not full_check:
        # Try to fetch EC2 data from Redis
        ec2_data = await get_from_redis("ec2_data")
        if ec2_data:
            return {"instances": ec2_data}
        
    instances_by_region = get_ec2_instances()

    if not instances_by_region:
        # Return an empty response instead of raising an error
        return {"instances": []}

    # Delegate the security check logic to the function
    checked_instances = ec2_security_check(instances_by_region)
    await save_to_redis("ec2_data", checked_instances)
    await update_service_data("ec2")
    return {"instances": checked_instances}
 