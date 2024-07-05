import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
from sqlalchemy.orm import Session
from starlette.requests import Request

from server import CIPHER
from server.com.ext.helper import send_response
from server.model.system import Ssid, System


class Authorize:
    SYSTEM = 0
    USER = 1


def create_token(uid, token_type):
    encoded_user_id = CIPHER.url_encode(uid)
    expire_time = datetime.utcnow() + timedelta(days=7)

    data = dict(exp=expire_time, user_hash=encoded_user_id, authorized=token_type)
    access_token = jwt.encode(data, os.getenv('SECRET_KEY', 'password'), algorithm="HS256")

    return access_token


def token_required(token_type):
    def decorator(fn):
        @wraps(fn)
        async def validation(*args, **kwargs):

            try:
                if not isinstance(args[0], Request) or not (token := args[0].headers.get('Authorization')):
                    return send_response({'message': 'Authorization was missing on request!'}, 401)
                db: Session = args[0].state.db

                payload = jwt.decode(token, os.getenv('SECRET_KEY', 'password'), algorithms=["HS256"])

                uid: str = CIPHER.url_decode(payload['user_hash'])
                ssids = db.query(Ssid).filter_by(ssid_uid=uid).all()
                cuid_idx = next(
                    (index for index, ssid in enumerate(ssids) if CIPHER.verify_hash(token, ssid.ssid_hash)),
                    None)
                if not cuid_idx:
                    return send_response({'message': 'Session expired, login again!'}, 401)
                if payload['authorized'] != token_type:
                    return send_response({'message': 'Access level unsatisfied!'}, 401)

                return await fn(*args, db, ssids[cuid_idx] ** kwargs)  # Use await here
            except jwt.PyJWTError:
                return send_response({'message': 'Invalid token, login again!'}, 401)

        return validation

    return decorator


def create_verification_link(user_email, base_url="https://yourdomain.com/verify"):
    token = generate_token()
    verification_link = f"{base_url}?email={user_email}&token={token}"
    return verification_link, token