class Config(object):
    SECRET_KEY='Clave nueva'
    SESSION_COOKIE_SECURE= False
    
class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/bdidgs802'
SQLALCHEMY_TRACK_MODIFICATIONS = False
