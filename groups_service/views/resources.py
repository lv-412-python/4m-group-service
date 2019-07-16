"""API routes"""
from groups_service import API
from .groups import (
    GroupResource
)

API.add_resource(GroupResource, '/group', '/group/<int:group_id>')
