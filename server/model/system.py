from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, VARCHAR, TIMESTAMP, INTEGER, ForeignKey, SMALLINT
from sqlalchemy.orm import relationship

from server.__main__ import Base


class System(Base):
    __tablename__ = "system"

    sid = Column(INTEGER(), autoincrement=True, primary_key=True)
    sys_uid = Column(VARCHAR(), nullable=False, unique=True)
    sys_name = Column(VARCHAR(), nullable=False)
    sys_username = Column(VARCHAR(), nullable=False, unique=True)
    sys_password = Column(VARCHAR(), nullable=False)
    created_at = Column(TIMESTAMP())
    updated_at = Column(TIMESTAMP())


class Node(Base):
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