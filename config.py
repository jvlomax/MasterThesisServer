class Config:
    SECRET_KEY = "SUPER SECRET KEY THAT NO ONE CAN FIND"


class DevConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'


class TestConfig(Config):
    DEBUG = False
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = Falseb