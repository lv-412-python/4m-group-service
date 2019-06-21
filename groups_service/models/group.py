"""Model for group service."""
import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String
)
from groups_service.db import DB



class GroupsModel(DB.Model): # pylint: disable=too-few-public-methods
    """Implementation of Group entity."""
    id = Column(Integer(), primary_key=True)
    title = Column(String(200), nullable=False, unique=True)
    form_id = Column(Integer(), nullable=True)
    owner_id = Column(Integer(), nullable=False)
    members = Column(String(25))
    date = Column(DateTime(), default=datetime.datetime.utcnow())

    def __init__(self, title, form_id, owner_id, members):
        self.title = title
        self.form_id = form_id
        self.owner_id = owner_id
        self.members = members
