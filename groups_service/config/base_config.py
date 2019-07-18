"""Configuration for group service."""

class Config:
    """
    Implementation of Configuration class.
    """
    DEBAG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI =\
    'postgres://postgres:mysecretpassword@172.17.0.2:5432/4m_groups'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
