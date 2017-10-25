import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'black firtizer can vapper'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_POSTS_PER_PAGE = 20

    MAIL_SERVER = 'smtp.126.com'
    MAIL_TLS = True
    MAIL_USERNAME = 'wujunjames@126.com'
    MAIL_PASSWORD = 'b925febe'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Fishry Admin <wujunjames@126.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:woods@localhost/fishry_dev?charset=utf8'
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:woods@localhost/fishry_test?charset=utf8mb4'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:woods@localhost/fishry_db?charset=utf8mb4'

config = {
        'default': DevelopConfig,
        'development': DevelopConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        }
