import datetime

from sqlalchemy.orm import Session
from starlette.requests import Request

from server.__main__ import app, cipher

from server.com.ext.helper import send_response
from server.model.user import User


@app.route('/api/v1/node/authorize/{auth}', methods=['POST'])
async def user_authorize(request: Request):
    enc_str = request.path_params.get('auth')
    device_id = request.query_params.get('device_id')

    db: Session = request.state.db
    node_uuid = cipher.url_decode(enc_str)
    user = User()
    user.device_id = device_id
    user.ip_address = f"{request.client.host}:{request.client.port}"
    user.node_uid = node_uuid
    user.joined_at = datetime.datetime.now()
    db.add(user)
    db.commit()

    return send_response({'data': [{'node_id': node_uuid}], "message": "Successfully authorized!"})
