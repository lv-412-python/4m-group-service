"""Serializers for group service."""
from groups_service import MA

class GroupsSchema(MA.Schema): # pylint: disable=too-few-public-methods
    """Implementation of Group schema."""
    class Meta:  # pylint: disable=too-few-public-methods
        """Implementation of Meta class with fields, we want to show."""
        fields = ('id', 'title', 'form_id', 'owner_id', 'members', 'date')

GROUP_SCHEMA = GroupsSchema(strict=True)
GROUPS_SCHEMA = GroupsSchema(many=True, strict=True)
