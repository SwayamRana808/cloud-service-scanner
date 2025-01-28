from fastapi import FastAPI,Request
from app.routes.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ec2_routes import scan_ec2_instances
from app.routes.iam_routes import scan_iam
from app.routes.nacl_routes import scan_network_acls
from app.routes.rds_routes import scan_rds
from app.routes.s3_bucket_routes import scan_s3
from app.routes.security_group_routes import fetch_and_analyze_security_groups
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dashboard import router as dashboard_router


# Initialize the scheduler
scheduler = AsyncIOScheduler()

async def update_redis_data():
    await scan_ec2_instances(full_check=True)
    await scan_iam(full_check=True)
    await scan_network_acls(full_check=True)
    await scan_rds(full_check=True)
    await scan_s3(full_check=True)
    await fetch_and_analyze_security_groups(full_check=True)


# Define the lifespan context manager
async def lifespan(app: FastAPI):
    # startup method to start the scheduler and perform initial tasks
    async def startup():
        print("Starting scheduler...")
        scheduler.start()

        # Perform an initial update when the application starts
        asyncio.create_task(update_redis_data())

    # shutdown method to stop the scheduler
    async def shutdown():
        print("Shutting down scheduler...")
        scheduler.shutdown()

    # Call startup and shutdown during the lifespan of the app
    await startup()
    yield
    await shutdown()


# Initialize the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


# CORS settings to allow frontend requests from localhost:3000
origins = [
    "http://localhost:3000",  # Allow requests from localhost:3000
]

# Add CORSMiddleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Register routes
app.include_router(api_router)
app.include_router(dashboard_router)


templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return """
    <h1>
        <a href="/dashboard">
            <button style="padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; text-decoration: none;">
                Go to Dashboard
            </button>
        </a>
    </h1>
    """




# Add a job to run `update_redis_data` every 10 minutes
scheduler.add_job(update_redis_data, "interval", minutes=2)
