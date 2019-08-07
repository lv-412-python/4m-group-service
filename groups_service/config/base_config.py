"""Configuration for group service."""
PG_DOCKER_DATABASE = 'postgres://postgres:mysecretpassword@db:5432/4m_groups'
LOCAL_DATABASE_URI = 'postgres://postgres:postgres@127.0.0.1:5432/4m_groups'
class Config:
    """
    Implementation of Configuration class.
    """
    DEBAG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = PG_DOCKER_DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = True
