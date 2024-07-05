from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, INTEGER, VARCHAR, TIMESTAMP, SMALLINT, ForeignKey
from sqlalchemy.orm import relationship

from server import MODEL


class Node(MODEL):
    __tablename__ = "node"

    nid = Column(INTEGER(), autoincrement=True, primary_key=True)
    node_uid = Column(VARCHAR(), nullable=False, unique=True)
    node_name = Column(VARCHAR(), nullable=False)
    node_qrc = Column(VARCHAR(), nullable=False)
    node_state = Column(SMALLINT(), default=0)
    created_at = Column(TIMESTAMP())
    expired_at = Column(TIMESTAMP())
    updated_at = Column(TIMESTAMP())

    sys_uid = Column(VARCHAR(), ForeignKey('system.sys_uid', ondelete='CASCADE'))
    sid_fk = relationship("System", foreign_keys=[sys_uid])


class NodeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Node
        include_fk = True
        additional = ['sys_name', 'sys_uid', 'sys_username', 'created_at']
        exclude = ['nid']
