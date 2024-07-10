import datetime

from sqlalchemy.orm import Session
from starlette.requests import Request

from server import CIPHER, app
from server.com.ext.helper import send_response
from server.model.node import Node
from server.model.user import User
from server.util.misc import requestor_metadata


@app.route('/api/v1/node/authorize/{auth}', methods=['POST'])
async def user_authorize(request: Request):
    enc_str = request.path_params.get('auth')
    db: Session = request.state.db
    node_uuid = CIPHER.url_decode(enc_str)

    node_detail = db.query(Node).filter_by(node_uid=node_uuid).first()
    if not node_detail or node_detail.node_state != 1 or node_detail.expired_at < datetime.datetime.now():
        return send_response({'message': 'Event was ended or not found!'})
    user = User()
    metadata = requestor_metadata(request)
    user.ip_address = metadata['requestor_ip']
    user.device = metadata['device_name']
    user.platform = metadata['os_name']
    user.browser = metadata['browser_name']
    user.node_uid = node_uuid
    user.joined_at = datetime.datetime.now()
    db.add(user)
    db.commit()

    return send_response({'data': [{'node_id': node_uuid}], "message": "Successfully authorized!"})
