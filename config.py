import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    SSL_DISABLE = False
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    BABEL_DEFAULT_LOCALE = 'zh'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024

    def __init__(self):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    HOST = '0.0.0.0'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    def __init__(self):
        BaseConfig.__init__(self)


class ProductConfig(BaseConfig):
    DEBUG = False
    HOST = '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/xiuchundao_site' #os.environ.get('XIUCHUNDAO_SITE_DATABASE_URL')

    def __init__(self):
        BaseConfig.__init__(self)


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'product': ProductConfig
}
