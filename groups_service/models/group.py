"""Model for group service."""
import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship, backref
from groups_service.db import DB


GROUP_FORM = Table('group_form', DB.metadata,
                   Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
                   Column('form_id', Integer, ForeignKey('forms.id'), primary_key=True))

class Groups(DB.Model):#pylint: disable=too-few-public-methods
    """Implementation for groups entity"""
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), unique=True)
    owner_id = Column(Integer())
    members = Column(String(200))
    date = Column(DateTime(), default=datetime.datetime.utcnow())

    def __init__(self, title, owner_id, members):
        self.title = title
        self.owner_id = owner_id
        self.members = members

class Forms(DB.Model):#pylint: disable=too-few-public-methods
    """Implementation table for form_id"""
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer(), unique=True)
    assigned_group = relationship('Groups', secondary=GROUP_FORM,
                                  backref=backref('form', lazy='dynamic'))

    def __init__(self, form_id):
        self.form_id = form_id
