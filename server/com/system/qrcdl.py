import json
import os

from starlette.requests import Request

from server.__main__ import app, cipher
from server.com.ext.helper import send_response, send_file

file_download = "/api/v1/file"


@app.route(file_download, methods=['GET'])
def qrc_download(request: Request):
    content = request.query_params.get('content', '')
    if not (data_str := cipher.decrypt(content)):
        return send_response({'message': 'File May Corrupted!'}, 400)
    file_md = json.loads(data_str)
    if os.path.exists(user_dir := os.path.join(os.getcwd(), os.getenv('QRC_PATH', 'qrc'), f"{file_md['uuid']}")):
        file_path = os.path.join(user_dir, file_md['file_name'])
        return send_file(file_path, file_md['legacy_name'])
    return send_response({'message': 'File Not Found!'}, 400)


def dl_url(request: Request) -> str:
    base_url = str(request.base_url)
    download_url = app.url_path_for('qrc_download').lstrip('/')
    return f"{base_url}{download_url}?content="
