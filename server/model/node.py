from sqlalchemy import Column, INTEGER, VARCHAR, TIMESTAMP

from server import MODEL


class Ssid(MODEL):
    __tablename__ = "ssid"
    id = Column(INTEGER(), autoincrement=True, primary_key=True)
    ssid_uid = Column(VARCHAR(), nullable=False, unique=True)
    ssid_hash = Column(VARCHAR(), nullable=False, unique=True)
    created_at = Column(TIMESTAMP())
    updated_at = Column(TIMESTAMP())
