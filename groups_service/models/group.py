"""Model for group service."""
import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from groups_service.db import DB


class Groups(DB.Model):#pylint: disable=too-few-public-methods
    """Implementation for groups entity."""
    __tablename__ = 'groups'
    id = Column(Integer(), primary_key=True)
    title = Column(String(200), unique=True)
    owner_id = Column(Integer())
    members = Column(String(200))
    date = Column(DateTime(), default=datetime.datetime.utcnow())
    assigned_to_forms = relationship('Forms', backref='group', lazy='dynamic')

    def __init__(self, title, owner_id, members, assigned_to_forms=None):
        self.title = title
        self.owner_id = owner_id
        self.members = members
        self.assigned_to_forms = assigned_to_forms

class Forms(DB.Model):#pylint: disable=too-few-public-methods
    """Implementation table for form."""
    __tablename__ = 'forms'
    id = Column(Integer(), primary_key=True)
    group_id = Column(Integer(), ForeignKey('groups.id'))
    form_id = Column(Integer())

    def __init__(self, form_id):
        self.form_id = form_id
