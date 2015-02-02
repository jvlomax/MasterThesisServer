class MasterConfig:
    SECRET_KEY = "SUPER SECRET KEY THAT NO ONE CAN FIND"


class DevConfig(MasterConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'


class TestConfig(MasterConfig):
    DEBUG = False
    TESTING = True


class ProductionConfig(MasterConfig):
    DEBUG = False
    TESTING = False