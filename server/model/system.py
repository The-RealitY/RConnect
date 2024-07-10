from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, VARCHAR, TIMESTAMP, INTEGER, SMALLINT

from server import MODEL


class System(MODEL):
    __tablename__ = "system"

    sid = Column(INTEGER(), autoincrement=True, primary_key=True)
    sys_uid = Column(VARCHAR(15), nullable=False, unique=True)
    sys_name = Column(VARCHAR(100), nullable=False)
    sys_username = Column(VARCHAR(12), nullable=False, unique=True)
    sys_email = Column(VARCHAR(100), nullable=False, unique=True)
    sys_password = Column(VARCHAR(100), nullable=False)
    sys_state = Column(SMALLINT(), default=0)
    created_at = Column(TIMESTAMP(), default=datetime.now())
    updated_at = Column(TIMESTAMP(), onupdate=datetime.now())


class Ssid(MODEL):
    __tablename__ = "ssid"
    id = Column(INTEGER(), autoincrement=True, primary_key=True)
    ssid_uid = Column(VARCHAR(), nullable=False)
    ssid_hash = Column(VARCHAR(), nullable=False, unique=True)
    ssid_ip = Column(VARCHAR())
    ssid_device = Column(VARCHAR())
    ssid_platform = Column(VARCHAR())
    ssid_browser = Column(VARCHAR())
    ssid_status = Column(VARCHAR(), default=1)
    created_at = Column(TIMESTAMP(), default=datetime.now())
    updated_at = Column(TIMESTAMP(), onupdate=datetime.now())


class SsidSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ssid
        exclude = ['id', 'ssid_uid', 'ssid_hash', 'updated_at']
