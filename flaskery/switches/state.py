# Copyright 2015 Jason Heeris <jason.heeris@gmail.com>
# 
# This file is part of the 'flaskery' application, and is licensed under the MIT
# license.
"""
The Flaskery app's state is two independent booleans ie. (boolean, boolean). It
defaults to both False.
"""
from alchy import ModelBase, make_declarative_base
from sqlalchemy import orm, Column, types, sql

Model = make_declarative_base(Base=ModelBase)

class SwitchesState(Model):

    __tablename__ = 'switches'

    id      = Column(types.Integer(), primary_key=True)
    one     = Column(types.Boolean(), nullable=False)
    two     = Column(types.Boolean(), nullable=False)
    touched = Column(
        types.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sql.func.now(),
        onupdate=sql.func.now())

    def __init__(self):
        self.one = False
        self.two = False
