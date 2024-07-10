import datetime
import json
import re
import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette.requests import Request

from server import app, CIPHER, AUTO_VERIFY, SMTP_SERVER, SMTP_PORT, SMTP_LOGIN, SMTP_PASSWORD, \
    SMTP_SENDER
from server.com.ext.helper import send_response
from server.com.ext.mail import Mail
from server.com.ext.validation import Authorize, create_token, token_required
from server.model.system import Ssid, SsidSchema
from server.model.system import System
from server.util.misc import requestor_metadata


def generate_verification_link(request, sys_uid):
    data = {
        'exp': str((datetime.datetime.now() + datetime.timedelta(minutes=30)).timestamp()),
        'token': CIPHER.url_encode(sys_uid)
    }
    enc_data = json.dumps(data)
    token = CIPHER.encrypt(enc_data)
    activation_link = f"{str(request.base_url)}{str(app.url_path_for('system_activation', verify_token=token)).lstrip('/')}"
    return activation_link


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
    system_detail.sys_state = 1 if AUTO_VERIFY else 0
    if not AUTO_VERIFY:
        verification_link = generate_verification_link(request, system_detail.sys_uid)
        Mail(SMTP_SERVER, SMTP_PORT, SMTP_LOGIN, SMTP_PASSWORD, SMTP_SENDER, recipient=email.strip()).send_mail(
            activation_link=verification_link)
    db.add(system_detail)
    db.commit()

    return send_response(
        {
            'message': "An Account Activation Was Sent To You Email.!" if not AUTO_VERIFY else "Account Created Successfully"
        },
        status=201
    )


@app.route('/api/v1/system/activation/{verify_token}', methods=['GET'])
async def system_activation(request: Request):
    db: Session = request.state.db
    verify_token = request.path_params.get('verify_token')

    datas = CIPHER.decrypt(verify_token)
    data = json.loads(datas)
    timestamp = float(data['exp'])
    expiration_time = datetime.datetime.fromtimestamp(timestamp)
    current_time = datetime.datetime.now()
    if current_time > expiration_time:
        return send_response({'message': 'Link Already Expired'}, status=400)
    sys = db.query(System).filter_by(sys_uid=CIPHER.url_decode(data['token'])).first()
    if not sys:
        return send_response({'message': 'Account Not Found!'}, 400)
    if sys.sys_state == 1:
        return send_response({'message': 'Account Already Activated!'}, 400)
    sys.sys_state = 1
    db.add(sys)
    db.commit()
    return send_response({'message': 'Account Successfully Activated, Close it Page.'}, 302)


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
    metadata = requestor_metadata(request)
    ssid.ssid_ip = metadata['requestor_ip']
    ssid.ssid_device = metadata['device_name']
    ssid.ssid_platform = metadata['os_name']
    ssid.ssid_browser = metadata['browser_name']
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


@app.route('/api/v1/system/session', methods=['GET'])
@token_required(Authorize.SYSTEM)
async def system_session(_, db: Session, ssid: Ssid):
    ses_data = db.query(Ssid).filter_by(ssid_uid=ssid.ssid_uid).all()
    data = SsidSchema().dump(ses_data, many=True)
    return send_response({'data': data, 'message': 'All Active Session Fetched Successfully'})


@app.route('/api/v1/system/sign-out', methods=['POST'])
@token_required(Authorize.SYSTEM)
async def system_sign_out(request: Request, db: Session, ssid: Ssid):
    if (mode := int(request.query_params.get('session', 0))) == 1:
        db.delete(ssid)
        db.commit()
        return send_response({'message': 'Successfully logged out.'})
    elif mode == 2:
        sessions = db.query(Ssid).filter_by(ssid_uid=ssid.ssid_uid).all()
        for session in sessions:
            db.delete(session)
            db.commit()
        return send_response({'message': 'Successfully logged out from all devices.'})
    else:
        return send_response({'message': 'An Error Occurred while logging out'}, 400)
