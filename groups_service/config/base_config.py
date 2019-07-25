"""Configuration for group service."""

class Config:
    """
    Implementation of Configuration class.
    """
    DEBAG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:mysecretpassword@db:5432/4m_groups'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
