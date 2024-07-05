import datetime
import re
import time
import uuid

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from starlette.requests import Request

from server import LOGGER, SERVER_UPTIME, app, CIPHER
from server.com.ext.helper import send_response
from server.com.ext.validation import Authorize, create_token, token_required
from server.model.system import Ssid
from server.model.system import System


@app.route('/', methods=['GET'])
async def index(request: Request):
    LOGGER.info("HAI")
    return send_response(
        {
            "data": [{
                'upTime': time.time() - SERVER_UPTIME
            }],
            'message': "Server was up and runnning!"

        },
        200
    )


@app.route('/api/v1/system/sign-up', methods=['POST'])
async def system_signup(request: Request):
    data: dict = await request.json()
    db: Session = request.state.db
    user_name = str(data.get('sys_username').strip().lower())
    if not re.match("^[A-Za-z0-9_]*$", user_name) or len(user_name) > 12:
        return send_response({
            'message': 'username must be 12 character length\n Only alphabets,numeric,special character "_" are allowed'},
            status=400)

    system_detail = db.query(System).filter(
        or_(System.sys_username == user_name, System.sys_email == (email := data['sys_email']))).first()
    if system_detail:
        return send_response({'message': 'Username Or Email Was Already Exists!'}, 400)
    system_detail = System()
    system_detail.sys_uid = str(uuid.uuid4()).replace('-', '').upper()[:10]
    system_detail.sys_name = data['sys_name']
    system_detail.sys_username = user_name
    system_detail.sys_email = email.strip()
    system_detail.sys_password = CIPHER.generate_hash(data['sys_password'])
    system_detail.created_at = datetime.datetime.now()

    db.add(system_detail)
    db.commit()
    return send_response(
        {'message': "An Account Activation Was Sent To You Email.!"
         },
        status=201
    )


@app.route('/api/v1/system/sign-in', methods=['POST'])
async def system_signin(request: Request):
    data: dict = await request.json()
    db: Session = request.state.db
    user_name = str(data.get('sys_username').strip().lower())[:12]
    password = str(data.get('sys_password', ''))
    system_detail = db.query(System).filter_by(sys_username=user_name).first()
    if not system_detail:
        return send_response({'message': 'User Not Exists!'}, 400)
    if system_detail.sys_state != 1:
        return send_response({'message': "Activate the account to continue!"}, 400)
    if not CIPHER.verify_hash(password, system_detail.sys_password):
        return send_response({'message': 'Wrong Credentials!'}, 400)
    ssid = db.query(Ssid).filter(Ssid.ssid_uid == str(system_detail.sys_uid)).all()
    if len(ssid) > 5:
        return send_response({'message': 'Maximum Session Reached, Logout previous session to proceed'},
                             403)
    ssid = Ssid()
    ssid.ssid_uid = str(system_detail.sys_uid)
    ssid.created_at = datetime.datetime.now()
    access_token = create_token(system_detail.sys_uid, Authorize.SYSTEM)
    ssid.ssid_hash = CIPHER.generate_hash(access_token)
    ssid.ssid_ip = "1"
    ssid.ssid_device = "1"
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


@app.route('/api/v1/system/sign-out', methods=['POST'])
@token_required(Authorize.SYSTEM)
async def system_signout(request: Request, db: Session, ssid: Ssid):
    if (mode := request.query_params.get('session')) == 1:
        db.delete(ssid)
    elif mode == 2:
        session = db.query(Ssid).filter_by(ssid_uid=ssid.ssid_uid).all()
        _ = (db.delete(lop_session) for lop_session in session)
    else:
        return send_response({'message': 'An Error Occurred while logging out'}, 400)
    db.commit()
    return send_response({'content': 'Successfully logged out from all devices.'})
