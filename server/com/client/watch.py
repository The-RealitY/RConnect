import asyncio
import datetime
import os

from fastapi import WebSocket
from sqlalchemy.orm import Session
from watchfiles import awatch

from server import app, SESSION
from server.model.node import Node


@app.websocket('/ws/v1/node/watch')
async def file_connect(websocket: WebSocket):
    node_uid: str = websocket.query_params.get('node_uid')
    db: Session = SESSION()
    node_detail = db.query(Node).filter_by(node_uid=node_uid).first()
    if not node_detail or node_detail.node_state != 1 or node_detail.expired_at < datetime.datetime.now():
        return await websocket.close(reason="Event not found or expired!", code=400)
    folder_path = os.path.join(os.getenv('NODE_PATH', 'Node'), node_detail.node_uid)
    os.makedirs(folder_path, exist_ok=True)
    try:
        await websocket.accept()
        await websocket.send_json({'message': f'Successfully Connected to {node_detail.node_name}'})
        async for _ in aiter(awatch(folder_path)):
            await websocket.send_json({'message': 'REFRESH_REQUIRED'})
    except asyncio.CancelledError:
        return await websocket.close(reason="Connection lost!", code=503)
