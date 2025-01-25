from fastapi import FastAPI
from app.routes.scan import router as scan_router

app = FastAPI()

# Register routes
app.include_router(scan_router)

@app.get("/")
def read_root():
    return {"message": "Cloud Service Misconfiguration Scanner is running."}
