"""Serializers for group service."""
from marshmallow import fields, post_load, pre_dump, pre_load
from groups_service import MA

class FormsSchema(MA.Schema):# pylint: disable=too-few-public-methods
    """Implementation of Forms schema."""
    form_id = fields.Integer()

    @pre_load
    def convert_int_to_dict(self, data):#pylint: disable=no-self-use
        """Converts into dict from int."""
        data = {'form_id': data}
        return data


class GroupsSchema(MA.Schema): # pylint: disable=too-few-public-methods
    """Implementation of Group schema."""
    id = fields.Integer(dump_only=True)
    title = fields.String()
    owner_id = fields.Integer()
    members = fields.List(fields.Integer())
    date = fields.Time(dump_only=True)
    assigned_to_forms = fields.Nested(FormsSchema, only='form_id', many=True)

    @post_load
    def conver_list_by_str(self, data):#pylint: disable=no-self-use
        """Converts into list from string."""
        if data.get('members'):
            data['members'] = ",".join(map(str, data['members']))
        return data

    @pre_dump
    def convert_str_by_list(self, data):#pylint: disable=no-self-use
        """Converts into string from list."""
        if data:
            data.members = list(map(int, data.members.split(',')))
        return data

class WorkerSchema(MA.Schema):
    """Implementation of Worker schema."""
    id = fields.Integer()
    title = fields.String()
    members = fields.List(fields.Integer())

    @pre_dump
    def convert_str_by_list(self, data):#pylint: disable=no-self-use
        """Converts into string from list."""
        data.members = list(map(int, data.members.split(',')))
        return data



GROUP_SCHEMA = GroupsSchema(strict=True)
GROUPS_SCHEMA = GroupsSchema(many=True, strict=True)
WORKER_SCHEMA = WorkerSchema(many=True, strict=True)
