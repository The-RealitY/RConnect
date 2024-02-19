import datetime
import uuid

from sqlalchemy.orm import Session
from starlette.requests import Request

from server.__main__ import app, cipher
from server.com.ext.helper import send_response
from server.com.ext.validation import Authorize, create_token
from server.model.node import Ssid
from server.model.system import System


@app.route('/api/v1/system/signup', methods=['POST'])
async def system_signup(request: Request):
    data: dict = await request.json()
    db: Session = request.state.db
    user_name = str(data.get('sys_username').strip().lower())[:12]
    system_detail = db.query(System).filter_by(sys_username=user_name).first()
    if system_detail:
        return send_response({'message': 'UserName Already Exists!'}, 400)
    system_detail = System()
    system_detail.sys_uid = str(uuid.uuid4()).replace('-', '').upper()[:10]
    system_detail.sys_name = data['sys_name']
    system_detail.sys_username = user_name
    system_detail.sys_password = cipher.generate_hash(data['sys_password'])
    system_detail.created_at = datetime.datetime.now()
    access_token = create_token(system_detail.sys_uid, Authorize.SYSTEM)

    # Session
    ses = db.query(Ssid).filter(Ssid.ssid_uid == str(system_detail.sys_uid)).first()
    if not ses:
        ses = Ssid()
        ses.created_at = datetime.datetime.now()
    ses.ssid_uid = system_detail.sys_uid
    ses.ssid_hash = cipher.generate_hash(access_token)

    db.add(system_detail)
    db.add(ses)
    db.commit()
    return send_response(
        {'data': [
            {'sys_uid': system_detail.sys_uid,
             'token': access_token
             }
        ],
            'message': "Account was created successfully!"
        }
    )


@app.route('/api/v1/system/signin', methods=['POST'])
async def system_signin(request: Request):
    data: dict = await request.json()
    db: Session = request.state.db
    user_name = str(data.get('sys_username').strip().lower())[:12]
    password = str(data.get('sys_password', ''))
    system_detail = db.query(System).filter_by(sys_username=user_name).first()
    if not system_detail:
        return send_response({'message': 'User Not Exists!'}, 400)
    if not cipher.verify_hash(password, system_detail.sys_password):
        return send_response({'message': 'Wrong Credentials!'}, 400)

    access_token = create_token(system_detail.sys_uid, Authorize.SYSTEM)
    ssid = db.query(Ssid).filter(Ssid.ssid_uid == str(system_detail.sys_uid)).first()
    if not ssid:
        ssid = Ssid()
        ssid.created_at = datetime.datetime.now()
    ssid.ssid_hash = cipher.generate_hash(access_token)
    ssid.updated_at = datetime.datetime.now()
    db.add(ssid)
    db.commit()
    return send_response(
        {'data': [
            {'sys_uid': system_detail.sys_uid,
             'token': access_token
             }
        ],
            'message': 'Successfully logged in!'
        }
    )
