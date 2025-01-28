from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from app.services.redis_service import get_from_redis
from datetime import datetime
import json

active_connections: List[WebSocket] = []

async def broadcast_data(service: str, data: dict):
    """Broadcast data to all active WebSocket connections."""
    def convert_datetime(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj

    serialized_data = json.dumps({"service": service, "data": data}, default=convert_datetime)
    for conn in active_connections:
        try:
            await conn.send_text(serialized_data)
            print(f"Sent data to {conn.client.host} ---- {service}")
        except WebSocketDisconnect:
            active_connections.remove(conn)

async def update_service_data(service: str):
    """Update WebSocket clients with the latest service data."""
    if service == "ec2":
        ec2_data = await get_from_redis("ec2_data")
        await broadcast_data(service, ec2_data)
    elif service == "iam":
        iam_data = await get_from_redis("iam_data")
        await broadcast_data(service, iam_data)
    elif service == "s3":
        s3_data = await get_from_redis("s3_data")
        await broadcast_data(service, s3_data)
    elif service == "nacl":
        nacl_data = await get_from_redis("nacl_data")
        await broadcast_data(service, nacl_data)
    elif service == "rds":
        rds_data = await get_from_redis("rds_data")
        await broadcast_data(service, rds_data)
    elif service == "sg":
        sg_data = await get_from_redis("security_groups_data")
        await broadcast_data(service, sg_data)

async def websocket_endpoint(websocket: WebSocket):
    """Manage WebSocket connections and handle disconnects."""
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)
