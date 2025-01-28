from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.services.redis_service import get_from_redis

router = APIRouter()

# Initialize the template rendering engine (Jinja2)
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def dashboard(request: Request):
    """
    API endpoint to display the dashboard with cloud service data.
    Fetches data from Redis for all services and renders the dashboard HTML page.
    """
    services = {}
    service_names = ["ec2_data", "s3_data", "iam_data", "rds_data","nacl_data","security_groups_data"]

    # Fetch data for each service from Redis
    for service_name in service_names:
        service_data = await get_from_redis(service_name)
        services[service_name] = service_data

    # Render the dashboard HTML template with the data
    return templates.TemplateResponse("dashboard.html", {"request": request, "services": services})
