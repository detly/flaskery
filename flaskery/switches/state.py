# Copyright 2015 Jason Heeris <jason.heeris@gmail.com>
# 
# This file is part of the 'flaskery' application, and is licensed under the MIT
# license.
"""
The Flaskery app's state is two independent booleans ie. (boolean, boolean). It
defaults to both False.
"""
from uuid import uuid4

from alchy import ModelBase, make_declarative_base
from sqlalchemy import orm, Column, types, sql

Model = make_declarative_base(Base=ModelBase)

class SwitchesState(Model):

    __tablename__ = 'switches'

    id      = Column(types.Integer(), primary_key=True)
    key     = Column(types.BINARY(length=16), nullable=False, unique=True)
    one     = Column(types.Boolean(), nullable=False)
    two     = Column(types.Boolean(), nullable=False)
    touched = Column(
        types.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sql.func.now(),
        onupdate=sql.func.now())

    def __init__(self):
        self.key = uuid4().bytes
        self.one = False
        self.two = False
