"""
Author: Humanpredator
CName: Event
BName: Node
"""

import datetime
import uuid

from sqlalchemy import case, and_
from sqlalchemy.orm import Session
from starlette.requests import Request

from server import app, CIPHER, QRCG
from server.com.ext.helper import send_response
from server.com.ext.validation import Authorize, token_required
from server.com.system.qrcdl import dl_url
from server.model.node import Node, NodeSchema
from server.model.system import System, Ssid


@app.route('/api/v1/system/node', methods=['POST'])
@token_required(Authorize.SYSTEM)
async def create_node(request: Request, db: Session, ssid: Ssid):
    data: dict = await request.json()
    sys_detail = db.query(System).filter_by(sys_uid=ssid.ssid_uid).first()
    if not sys_detail:
        return send_response({'message': 'User not found!'}, 400)

    node_detail = Node()
    node_detail.node_uid = str(uuid.uuid4()).replace('-', '').upper()[:10]
    node_detail.sys_uid = sys_detail.sys_uid
    node_detail.node_state = 1
    node_detail.node_name = data.get('node_name', 'System Generated')
    node_detail.created_at = datetime.datetime.utcnow()
    node_detail.expired_at = datetime.datetime.utcnow() + datetime.timedelta(days=int(data.get('expired_at', '10')))
    qr_data = f"{str(request.base_url)}{str(app.url_path_for('user_authorize', auth=CIPHER.url_encode(node_detail.node_uid))).lstrip('/')}"
    file_md = QRCG.generate_qrc(qr_data, node_detail.node_uid)
    node_detail.node_qrc = CIPHER.encrypt(file_md)
    db.add(node_detail)
    db.commit()

    return send_response({'data': [
        {'node_uid': node_detail.node_uid,
         'node_name': node_detail.node_name,
         'node_qrc': dl_url(request) + node_detail.node_qrc
         }
    ], 'message': 'Event was created successfully!'
    })


@app.route('/api/v1/system/node', methods=['GET'])
@token_required(Authorize.SYSTEM)
async def list_nodes(request: Request, db: Session, ssid: Ssid):
    details = db.query(Node).with_entities(
        Node.node_uid,
        Node.node_name,
        case(*[(Node.node_qrc.isnot(None),
                dl_url(request) + Node.node_qrc
                )
               ],
             else_=None).label('node_qrc'),
        Node.created_at,
        Node.nid,
        Node.expired_at,
        Node.node_state
    ).order_by(Node.nid.desc()).filter(
        Node.sys_uid == str(ssid.ssid_uid)
    ).all()

    data = NodeSchema().dump(details, many=True)
    return send_response({'data': data, 'message': 'Data fetched successful'})


@app.route('/api/v1/system/node', methods=['PUT'])
@token_required(Authorize.SYSTEM)
async def create_node(request: Request, db: Session, ssid: Ssid):
    state: int = int(request.query_params.get('node_state', '0'))
    node_uid: str = request.query_params.get('node_uid', None)
    node_detail = db.query(Node).filter(and_(
        Node.node_uid == node_uid,
        Node.sys_uid == ssid.ssid_uid
    )).first()
    if not node_detail:
        return send_response({'message': 'Node not found!'}, 400)
    if node_detail.expired_at < datetime.datetime.now():
        return send_response({'message': 'Node already expired!'}, 400)
    node_detail.node_state = state
    node_detail.updated_at = datetime.datetime.now()
    db.add(node_detail)
    db.commit()
    return send_response({'message': 'Node state updated successfully!'
                          })
