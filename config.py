import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = 'Erasmus'
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    template_folder = os.path.join(basedir, "app", "templates")
    static_folder = os.path.join(basedir, "app", "statics")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

    DB_HOST='127.0.0.1'
    DB_SCHEMA='erasmus'
    DB_USER='erasmus'
    DB_PWD='erasmus'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://{}:{}@{}/{}'.format(DB_USER, DB_PWD, DB_HOST, DB_SCHEMA)

    print('THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

    DB_HOST = '127.0.0.1'
    DB_SCHEMA = 'erasmus'
    DB_USER = 'erasmus'
    DB_PWD = 'erasmus'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://{}:{}@{}/{}?charset=utf8'.format(DB_USER, DB_PWD, DB_HOST, DB_SCHEMA)

    print('THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')


config = {
    "dev": DevelopmentConfig,
    "prod": Config,
    "test": TestConfig
}
