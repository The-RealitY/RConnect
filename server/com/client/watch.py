import asyncio
import datetime
import os

from fastapi import WebSocket
from sqlalchemy.orm import Session
from starlette.requests import Request
from watchfiles import awatch

from server import app, SESSION
from server.com.client.filem import file_baseurl
from server.com.ext.helper import send_response
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
    await websocket.accept()
    await websocket.send_json({'message': f'Successfully Connected to {node_detail.node_name}'})
    try:
        async for _ in aiter(awatch(folder_path)):
            await websocket.send_json({'message': 'REFRESH'})
    except asyncio.CancelledError:
        return await websocket.close(reason="Connection lost!", code=503)


@app.get('/api/v1/node/files')
async def event_files(request: Request):
    node_uid: str = request.query_params.get('node_uid')
    db: Session = SESSION()
    node_detail = db.query(Node).filter_by(node_uid=node_uid).first()
    if not node_detail or node_detail.node_state != 1 or node_detail.expired_at < datetime.datetime.now():
        return send_response({'message': 'Event expired or not found!'})

    folder_path = os.path.join(os.getenv('NODE_PATH', 'Node'), node_detail.node_uid)
    os.makedirs(folder_path, exist_ok=True)
    file_list = [{"thumbnail": file_baseurl(request, node_uid, f, 'T'),
                  "download": file_baseurl(request, node_uid, f, 'F')} for f in
                 os.listdir(folder_path) if
                 os.path.isfile(os.path.join(folder_path, f))]
    return send_response({'data': file_list, 'message': 'Files successfully updated!'}, 200)
