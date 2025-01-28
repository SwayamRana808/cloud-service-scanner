from fastapi import APIRouter, Request
from app.services.nacl_service import get_network_acls
from app.security.nacl_security_check import analyze_network_acls
from app.services.redis_service import save_to_redis, get_from_redis
from app.services.websocket_service import update_service_data
router = APIRouter()

@router.get("/get_nacls")
async def scan_network_acls(request: Request = None, full_check: bool = False):
    """
    API endpoint to fetch and analyze Network ACLs (NACLs) for security issues.
    """
    if request:
        full_check = request.headers.get("X-Full-Check", "false").lower() == "true"

    if not full_check:
        # Try to fetch NACL data from Redis
        nacls_data = await get_from_redis("nacl_data")
        if nacls_data:
            return {"results": nacls_data}
        

    nacls_by_region = get_network_acls()
    if not nacls_by_region:
        # Return an empty response instead of raising an error
        return {"results": []}

    results = {}

    for region, nacls in nacls_by_region.items():
        if isinstance(nacls, dict) and "error" in nacls:
            # Handle errors
            results[region] = {"error": nacls["error"]}
        else:
            # Analyze NACLs and include issues
            analyzed_nacls = analyze_network_acls(nacls)
            results[region] = analyzed_nacls

    await save_to_redis("nacl_data", results)
    await update_service_data("nacl")
    return {"results": results}
