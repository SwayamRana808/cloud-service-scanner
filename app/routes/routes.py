from fastapi import APIRouter
from app.routes.ec2_routes import router as ec2_router
from app.routes.iam_routes import router as iam_router
from app.routes.s3_bucket_routes import router as s3_router
from app.routes.rds_routes import router as rds_router
from app.routes.nacl_routes import router as nacl_router
from app.routes.security_group_routes import router as security_router
from app.routes.websocket_routes import websocket_router  
# Create a master router to include all sub-routers
router = APIRouter()

# Include individual routers
router.include_router(ec2_router, prefix="/api/ec2", tags=["EC2"])
router.include_router(iam_router, prefix="/api/iam", tags=["IAM"])
router.include_router(s3_router, prefix="/api/s3", tags=["S3"])
router.include_router(rds_router, prefix="/api/rds", tags=["RDS"])
router.include_router(nacl_router, prefix="/api/nacl", tags=["NACL"])
router.include_router(security_router, prefix="/api/security_groups", tags=["Sg"])

router.include_router(websocket_router,tags=["WebSocket"])