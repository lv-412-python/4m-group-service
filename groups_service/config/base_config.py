"""config"""

class Config:
    """
    Implementation of Configuration class.
    """
    DEBAG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/4m_groups'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
