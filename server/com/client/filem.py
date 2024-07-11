import datetime
import os
import uuid
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path

from PIL import Image
from fastapi import File, UploadFile, Request
from sqlalchemy.orm import Session

from server import app, SESSION
from server.com.ext.helper import send_response, send_file
from server.model.node import Node
from server.util.misc import remove_metadata


def create_thumbnail(ip, file_name, node_uuid, thumbnail_size=(100, 100)):
    tn_path = os.path.join(os.getenv('NODE_PATH', 'Node'), node_uuid, '.thumbnail')
    os.makedirs(tn_path, exist_ok=True)
    original_image = Image.open(ip)
    original_image.thumbnail(thumbnail_size)
    original_image.save(os.path.join(tn_path, file_name))


def process_upload(file, folder_path, node_uuid):
    file_extension = Path(file.filename).suffix
    nw_fn = str(uuid.uuid4()) + file_extension
    img_path = os.path.join(folder_path, nw_fn)
    file.file.seek(0)
    with open(img_path, "wb") as f:
        file_content = file.file.read()
        file_br = remove_metadata(file_content)
        f.write(file_br)

    create_thumbnail(img_path, nw_fn, node_uuid)


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


@app.post("/api/v1/node/upload-file")
async def upload_file(
        request: Request,
        file: UploadFile = File(...)
):
    db: Session = request.state.db
    node_uuid = request.query_params.get('node_uid')
    node_detail = db.query(Node).filter_by(node_uid=node_uuid).first()

    if not node_detail or node_detail.node_state != 1 or node_detail.expired_at < datetime.datetime.now():
        return send_response({'message': 'Event was ended or not found!'})

    folder_path = os.path.join(os.getenv('NODE_PATH', 'Node'), node_detail.node_uid)
    os.makedirs(folder_path, exist_ok=True)
    with ThreadPoolExecutor() as executor:
        executor.submit(process_upload, file, folder_path, node_uuid)

    return send_response({'message': f'{file.filename} was processed successfully, soon uploaded.'})


@app.get('/api/v1/node/thumbnail/{node_uid}/{file}')
async def download_thumbnail(request: Request):
    node_uid = request.path_params.get('node_uid')
    file = request.path_params.get('file')
    if not os.path.exists((event_folder := os.path.join(os.getenv('NODE_PATH', 'Node'), node_uid))):
        return send_response({'message': 'Event expired or not found!'}, 400)
    if not os.path.exists(os.path.join(file_path := os.path.join(event_folder, '.thumbnail', file))):
        return send_response({'message': 'File not found!'}, 400)
    return send_file(file_path)


@app.get('/api/v1/node/media/{node_uid}/{file}')
async def download_file(request: Request):
    event_id = request.path_params.get('node_uid')
    file = request.path_params.get('file')
    if not os.path.exists((event_folder := os.path.join(os.getenv('NODE_PATH', 'Node'), event_id))):
        return send_response({'message': 'Event expired or not found!'}, 400)
    if not os.path.exists(os.path.join(file_path := os.path.join(event_folder, file))):
        return send_response({'message': 'File not found!'}, 400)
    return send_file(file_path)


def file_baseurl(request, node_uuid, file, svc="F"):
    base_url = str(request.base_url)
    return base_url + app.url_path_for(f"{'download_thumbnail' if svc == 'T' else 'download_file'}",
                                       node_uid=node_uuid, file=file).lstrip('/')
