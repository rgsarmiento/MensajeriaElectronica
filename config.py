class BaseConfig():
    SECRET_KEY = 'UXVpY2tseV9TZWNyZXRLZXk='#Quickly_SecretKey
    DEBUG=True
    TESTING = True

    SQLALCHEMY_DATABASE_URI =  'sqlite:///quickly.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Servidor de correo electronico
    MAIL_SERVER = "smtp-mail.outlook.com"
    MAIL_PORT = 587
    MAIL_USERNAME ="rgsarmiento@uninorte.edu.co"
    MAIL_PASSWORD ="89112652044Rg"
    MAIL_USE_TLS = False
    MAIL_USESSL = True

class DevelopmenConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    DEBUG=False
    TESTING = False

