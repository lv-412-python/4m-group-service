"""Group view implementation."""
from marshmallow import ValidationError, fields
from flask_api import status
from sqlalchemy.exc import IntegrityError
from flask import request, Response
from flask_restful import Resource, HTTPException
from webargs.flaskparser import parser

from groups_service import APP
from groups_service.db import DB
from groups_service.serializers import (
    GROUP_SCHEMA,
    GROUPS_SCHEMA,
    WORKER_SCHEMA
)
from groups_service.models.group import Groups, Forms

class GroupResource(Resource):
    """Class GroupView implementation."""
    def post(self):#pylint: disable=no-self-use
        """
        Post method for creating a new group.
        :return: Response object or error message with status code.
        """
        try:
            req = GROUP_SCHEMA.load(request.json).data
        except ValidationError as err:
            APP.logger.error(err.args)
            return err.messages, status.HTTP_400_BAD_REQUEST
        forms_id = req.pop('assigned_to_forms', None)
        list_forms = [Forms(form_id.get('form_id')) for form_id in forms_id] if forms_id else None
        if list_forms:
            req.update({'assigned_to_forms' : list_forms})
        new_group = Groups(**req)
        DB.session.add(new_group)
        try:
            DB.session.commit()
        except IntegrityError as err:
            APP.logger.error(err.args)
            DB.session.rollback()
            return {'error': 'Already exist'}, status.HTTP_400_BAD_REQUEST
        return Response(status=status.HTTP_201_CREATED)

    def get(self, group_id=None):# pylint: disable=no-self-use
        """
        Get method for Group Service.
        :return: requested groups with status code or error message with status code.
        """
        if group_id:
            group = Groups.query.get(group_id)
            result = GROUP_SCHEMA.dump(group).data
        else:
            url_args = {
                'groups': fields.List(fields.Integer(validate=lambda val: val > 0)),
                'owner': fields.List(fields.Integer(validate=lambda val: val > 0))
            }
            try:
                args = parser.parse(url_args, request)
            except HTTPException as err:
                APP.logger.error(err.args)
                return {'error': 'Invalid URL.'}, status.HTTP_400_BAD_REQUEST
            if args.get('groups'):
                title_groups = Groups.query.filter(
                    Groups.id.in_(args['groups'])
                    )
                result = WORKER_SCHEMA.dump(title_groups).data
            else:
                owner_groups = Groups.query.filter(Groups.owner_id.in_(args['owner']))
                result = GROUPS_SCHEMA.dump(owner_groups).data

        return (result, status.HTTP_200_OK) if result else \
               ({'error': 'Does not exist.'}, status.HTTP_404_NOT_FOUND)

    def put(self, group_id):#pylint: disable=no-self-use
        """
        Put method for the group.
        :return: Response object or error message with status code.
        """
        try:
            updated_data = GROUP_SCHEMA.load(request.json).data
        except ValidationError as err:
            APP.logger.error(err.args)
            return err.messages, status.HTTP_400_BAD_REQUEST

        updated_group = Groups.query.get(group_id)
        if updated_group is None:
            return {'error': 'Does not exist.'}, status.HTTP_404_NOT_FOUND

        forms_id = updated_data.pop('assigned_to_forms', None)
        list_forms = [Forms(form_id.get('form_id')) for form_id in forms_id] if forms_id else None
        if list_forms:
            updated_data.update({'assigned_to_forms' : list_forms})
        for key, value in updated_data.items():
            setattr(updated_group, key, value)
        DB.session.commit()

        return Response(status=status.HTTP_200_OK)
