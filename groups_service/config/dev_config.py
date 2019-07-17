""" Configuration for development."""
from groups_service.config.base_config import Config


class DevelopmentConfig(Config):
    """Class with development config."""
    DEVELOPMENT = True
    DEBUG = True
