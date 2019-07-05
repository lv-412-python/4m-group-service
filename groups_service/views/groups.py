'''Implementation groups_service'''
from marshmallow import ValidationError
from flask_api import status
from flask import request, jsonify, Response
from flask_restful import Resource
from groups_service.db import DB
from groups_service.serializers import (
    GROUP_SCHEMA,
    GROUPS_SCHEMA
)
from groups_service.models.group import Groups, Forms


OK = 200
BAD_REQUEST = 400
NOT_FOUND = 404

class GroupResource(Resource):
    '''Group resource.'''
    def post(self):#pylint: disable=no-self-use
        '''method post'''
        try:
            req = GROUP_SCHEMA.load(request.json).data
        except ValidationError as err:
            return jsonify(err.messages), status.HTTP_400_BAD_REQUEST
        form_id = req.pop('form_id', None)
        new_group = Groups(**req)
        if form_id:
            form = Forms.query.get(form_id)
            if not form:
                return {'error': 'Form not exist'}, status.HTTP_400_BAD_REQUEST
            new_group.forms.append(form)
        DB.session.add(new_group)
        DB.session.commit()
        message = {'message': 'Succsess'}, status.HTTP_201_CREATED
        return message

        # print(form, title, owner, members)

        # try:
        #     print('hello')
        #     DB.session.commit()
        # except IntegrityError as err:
        #     DB.session.rollback()
        #     return {'error': 'Already exist'}, status.HTTP_400_BAD_REQUEST
        # message = {'message': 'Succsess'}, status.HTTP_201_CREATED
        # return message

    def get(self):#pylint: disable=no-self-use
        '''Method get.'''
        resp = Response()
        groups = Groups.query.join(Groups.group).filter_by(groups_id=id).all()
        message = GROUPS_SCHEMA.dump(groups).data
        resp = jsonify(message)
        resp.status_code = status.HTTP_200_OK
    #     elif owner_id and not group_id:
    #         try:
    #             group = GroupsModel.query.filter_by(owner_id=owner_id)
    #             message = GROUPS_SCHEMA.dump(group).data
    #         except DataError:
    #             message = {'error': 'Invalid url.'}
    #             resp = jsonify(message)
    #             resp.status_code = status.HTTP_404_NOT_FOUND
    #         if not message:
    #             message = {'error': "Does not exist."}
    #             resp = jsonify(message)
    #             resp.status_code = status.HTTP_400_BAD_REQUEST
    #         else:
    #             resp = jsonify(message)
    #             resp.status_code = status.HTTP_200_OK
    #     else:
    #         try:
    #             group = GroupsModel.query.get(group_id)
    #             print(group)
    #         except DataError:
    #             message = {'error': 'Invalid url.'}
    #             resp = jsonify(message)
    #             resp.status_code = status.HTTP_404_NOT_FOUND
    #         if group is None:
    #             message = {'error': "Does not exist."}
    #             resp = jsonify(message)
    #             resp.status_code = status.HTTP_400_BAD_REQUEST
    #         else:
    #             message = GROUP_SCHEMA.dump(group).data
    #             resp = jsonify(message)
    #             resp.status_code = status.HTTP_200_OK
        return resp
