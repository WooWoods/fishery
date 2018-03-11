import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fat-peanut'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FISHERY_MAIL_SUBJECT_PREFIX = '[YANGTZ FISHERY]'
    FISHERY_MAIL_SENDER = 'Fishery Admin <fishery_admin@126.com>'
    FISHERY_ADMIN = os.environ.get('fishery_admin@126.com')
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.126.com'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:woods@localhost/fishery_dev?charset=utf8'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:woods@localhost/fishery?charset=utf8'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
