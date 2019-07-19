from groups_service.config.base_config import Config

class TestConfiguration(Config):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/4m_groups_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False