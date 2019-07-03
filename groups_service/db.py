'''Database connection.'''
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from groups_service import APP
from groups_service.config.dev_config import DevelopmentConfig



APP.config.from_object(DevelopmentConfig)
DB = SQLAlchemy(APP)

MIGRATE = Migrate(APP, DB)
