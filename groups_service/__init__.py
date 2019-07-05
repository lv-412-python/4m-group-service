"""Init groups service"""# pylint: disable=cyclic-import
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask import Flask

APP = Flask(__name__)
API = Api(APP)
MA = Marshmallow(APP)

from groups_service.views import resources
