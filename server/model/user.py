import datetime

from sqlalchemy import Column, VARCHAR, TIMESTAMP, INTEGER, ForeignKey
from sqlalchemy.orm import relationship

from server import MODEL


class User(MODEL):
    __tablename__ = "user"

    uid = Column(INTEGER(), autoincrement=True, primary_key=True)
    ip_address = Column(VARCHAR(100))
    device = Column(VARCHAR(100))
    platform = Column(VARCHAR(100))
    browser = Column(VARCHAR(100))
    joined_at = Column(TIMESTAMP(), onupdate=datetime.datetime.now())

    node_uid = Column(VARCHAR(15), ForeignKey('node.node_uid', ondelete='CASCADE'))
    node_uid_fk = relationship("Node", foreign_keys=[node_uid])
