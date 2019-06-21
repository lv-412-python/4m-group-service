"""Init groups service"""
from flask_marshmallow import Marshmallow
from flask import Flask

APP = Flask(__name__)
MA = Marshmallow(APP)

from groups_service.views.groups import (
    post_group,
    get_group,
    all_groups,
    get_groups_owner
)
