"""Configuration for production."""
from groups_service.config.base_config import Config

class ProductionConfig(Config):
    """Class with production config."""
    DEBUG = False
