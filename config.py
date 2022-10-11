class BaseConfig():
    SECRET_KEY = 'UXVpY2tseV9TZWNyZXRLZXk='#Quickly_SecretKey
    DEBUG=True
    TESTING = True

    SQLALCHEMY_DATABASE_URI =  'sqlite:///quickly.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False       

class DevelopmenConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    DEBUG=False
    TESTING = False

