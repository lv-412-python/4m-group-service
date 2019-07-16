'''Implementation groups_service'''
from marshmallow import ValidationError, fields
from flask_api import status
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify, Response
from flask_restful import Resource
from webargs.flaskparser import parser
from groups_service.db import DB
from groups_service.serializers import (
    GROUP_SCHEMA,
    GROUPS_SCHEMA,
    WORKER_SCHEMA
)
from groups_service.models.group import Groups, Forms

class GroupResource(Resource):
    '''Group resource.'''
    def post(self):#pylint: disable=no-self-use
        '''method post'''
        try:
            req = GROUP_SCHEMA.load(request.json).data
        except ValidationError as err:
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
            DB.session.rollback()
            return {'error': 'Already exist'}, status.HTTP_400_BAD_REQUEST
        return {'message': 'Succsess'}, status.HTTP_201_CREATED

    def get(self, group_id=None):# pylint: disable=no-self-use
        '''Method get.'''
        resp = Response()
        url_args = {
            'groups': fields.List(fields.Integer(validate=lambda val: val > 0))
        }
        args = parser.parse(url_args, request)
        if args:
            title_groups = Groups.query.with_entities(
                Groups.id, Groups.title
                ).filter(
                    Groups.id.in_(args['groups'])
                )
            try:
                res = WORKER_SCHEMA.dump(title_groups).data
            except ValidationError as err:
                return err.messages, status.HTTP_400_BAD_REQUEST
            return res, status.HTTP_200_OK

        if group_id:
            group = Groups.query.get(group_id)
            if group is None:
                message = {'error': "Does not exist."}
                resp = jsonify(message)
                resp.status_code = status.HTTP_400_BAD_REQUEST
            else:
                message = GROUP_SCHEMA.dump(group).data
                resp = jsonify(message)
                resp.status_code = status.HTTP_200_OK
        else:
            groups = Groups.query.all()
            message = GROUPS_SCHEMA.dump(groups).data
            resp = jsonify(message)
            resp.status_code = status.HTTP_200_OK
        return resp

    def put(self, group_id):#pylint: disable=no-self-use
        '''Method put.'''
        updated_group = Groups.query.get(group_id)
        if updated_group is None:
            return {'error': 'Does not exist.'}, status.HTTP_400_BAD_REQUEST
        try:
            updated_data = GROUP_SCHEMA.load(request.json).data
        except ValidationError as err:
            return err.messages, status.HTTP_400_BAD_REQUEST
        forms_id = updated_data.pop('assigned_to_forms', None)
        list_forms = [Forms(form_id.get('form_id')) for form_id in forms_id] if forms_id else None
        if list_forms:
            updated_data.update({'assigned_to_forms' : list_forms})
        for key, value in updated_data.items():
            setattr(updated_group, key, value)
        DB.session.commit()
        return Response(status=status.HTTP_200_OK)
