"""Serializers for group service."""
from marshmallow import fields, post_load, pre_dump
from groups_service import MA

class GroupsSchema(MA.Schema): # pylint: disable=too-few-public-methods
    """Implementation of Group schema."""
    id = fields.Integer(dump_only=True)
    title = fields.String()
    form_id = fields.Integer()
    owner_id = fields.Integer()
    members = fields.List(fields.Integer())
    date = fields.Time(dump_only=True)

    @post_load
    def conver_list_by_str(self, data):#pylint: disable=no-self-use
        '''conver_list_by_str'''
        data['members'] = ",".join(map(str, data['members']))
        return data

    @pre_dump
    def convert_str_by_list(self, data):#pylint: disable=no-self-use
        '''convert_str_by_list'''
        data.members = list(map(int, data.members.split(',')))
        return data

GROUP_SCHEMA = GroupsSchema(strict=True)
GROUPS_SCHEMA = GroupsSchema(many=True, strict=True)
