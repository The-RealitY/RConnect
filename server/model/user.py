import datetime

from sqlalchemy import Column, VARCHAR, TIMESTAMP, INTEGER, ForeignKey
from sqlalchemy.orm import relationship

from server import MODEL


class User(MODEL):
    __tablename__ = "user"

    uid = Column(INTEGER(), autoincrement=True, primary_key=True)
    ip_address = Column(VARCHAR())
    device = Column(VARCHAR())
    platform = Column(VARCHAR())
    browser = Column(VARCHAR())
    joined_at = Column(TIMESTAMP(), onupdate=datetime.datetime.now())

    node_uid = Column(VARCHAR(), ForeignKey('node.node_uid', ondelete='CASCADE'))
    node_uid_fk = relationship("Node", foreign_keys=[node_uid])
