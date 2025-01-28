from fastapi import APIRouter, WebSocket
from app.services.websocket_service import websocket_endpoint

websocket_router = APIRouter()

@websocket_router.websocket("/ws")
async def websocket_connection(websocket: WebSocket):
    """WebSocket connection for all services."""
    await websocket_endpoint(websocket)
