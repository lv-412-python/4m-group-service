""" development config """
from groups_service.config.base_config import Config


class DevelopmentConfig(Config):
    """ development config """
    DEVELOPMENT = True
    DEBUG = True
