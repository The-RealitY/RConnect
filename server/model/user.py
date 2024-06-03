import datetime

from sqlalchemy import Column, VARCHAR, TIMESTAMP, INTEGER, ForeignKey
from sqlalchemy.orm import relationship

from server import MODEL


class User(MODEL):
    __tablename__ = "user"

    uid = Column(INTEGER(), autoincrement=True, primary_key=True)
    device_id = Column(VARCHAR(), nullable=False)
    ip_address = Column(VARCHAR())
    joined_at = Column(TIMESTAMP(), onupdate=datetime.datetime.now())

    node_uid = Column(INTEGER(), ForeignKey('node.node_uid', ondelete='CASCADE'))
    node_uid_fk = relationship("Node", foreign_keys=[node_uid])
