from fastapi import APIRouter, Request
from app.services.security_group_service import get_security_groups
from app.security.security_group_security_check import analyze_security_groups
from app.services.redis_service import save_to_redis, get_from_redis
from app.services.websocket_service import update_service_data

router = APIRouter()

@router.get("/get_security_groups")
async def fetch_and_analyze_security_groups(request: Request = None, full_check: bool = False):
    """
    API endpoint to fetch and analyze security groups.
    """
    if request:
        full_check = request.headers.get("X-Full-Check", "false").lower() == "true"

    if not full_check:
        # Try to fetch Security Groups data from Redis
        security_groups_data = await get_from_redis("security_groups_data")
        if security_groups_data:
            return {"results": security_groups_data}

    security_groups_by_region = get_security_groups()
    all_security_groups_with_issues = {}

    for region, security_groups in security_groups_by_region.items():
        if isinstance(security_groups, dict) and "error" in security_groups:
            all_security_groups_with_issues[region] = {"error": security_groups["error"]}
        else:
            # Add issues to each security group
            for group in security_groups:
                group["Issues"] = analyze_security_groups(group)

            all_security_groups_with_issues[region] = security_groups
    await save_to_redis("security_groups_data", all_security_groups_with_issues)
    await update_service_data("sg")
    return {"results": all_security_groups_with_issues}

