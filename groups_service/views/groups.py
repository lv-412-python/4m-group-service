'''Implementation groups_service''' # pylint: disable=cyclic-import
from flask import request, jsonify
from groups_service import APP
from groups_service.db import DB
from groups_service.serializers import (
    GROUP_SCHEMA,
    GROUPS_SCHEMA
)
from groups_service.models.group import GroupsModel


@APP.route('/api/create_group', methods=['POST'])
def post_group():
    """Post method for Group."""
    title = request.json['title']
    form_id = request.json['form_id']
    owner_id = request.json['owner_id']
    members = request.json['members']

    members = ",".join(map(str, members))
    exists_group = bool(GroupsModel.query.filter_by(
        title=title,
        form_id=form_id,
        owner_id=owner_id,
        members=members
        ).first())
    if exists_group:
        message = jsonify({'message': 'Group alredy exists'}), 400
    else:
        new_group = GroupsModel(title, form_id, owner_id, members)
        DB.session.add(new_group)
        DB.session.commit()
        message = GROUP_SCHEMA.jsonify(new_group), 201
    return message

@APP.route('/api/groups', methods=['GET'])
def all_groups():
    """Get method for all groups."""
    groups = GroupsModel.query.all()
    result = jsonify(GROUPS_SCHEMA.dump(groups).data)
    return result

@APP.route('/api/group/<group_id>')
def get_group(group_id):
    """Get method for one group by group_id."""
    if group_id.isnumeric():
        group = GroupsModel.query.get_or_404(group_id)
        group.members = list(map(int, group.members.split(',')))
        message = GROUP_SCHEMA.jsonify(group)
    else:
        message = jsonify({'message': 'Not correct URL'}), 400
    return message

@APP.route('/api/groups/<owner_id>', methods=['GET'])
def get_groups_owner(owner_id):
    '''Get method for all groups by owner_id'''
    if owner_id.isnumeric():
        groups = GroupsModel.query.filter_by(owner_id=owner_id)
        for group in groups:
            group.members = list(map(int, group.members.split(',')))
        message = GROUPS_SCHEMA.jsonify(groups)
    else:
        message = jsonify({'message': 'Not correct URL'})
    return message
