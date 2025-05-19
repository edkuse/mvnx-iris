from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './iris/sessions'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # CSRF protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY') or 'csrf-secret-key'

    # Microsoft Entra ID (Azure AD) settings
    MS_CLIENT_ID = os.getenv('MS_CLIENT_ID')
    MS_CLIENT_SECRET = os.getenv('MS_CLIENT_SECRET')
    MS_TENANT_ID = os.getenv('MS_TENANT_ID')
    MS_AUTHORITY = f"https://login.microsoftonline.com/{MS_TENANT_ID}"
    MS_SCOPES = ["User.Read"]
    MS_GRAPH_API = "https://graph.microsoft.com"
    
    # Application settings
    APP_NAME = 'MVNx Iris'
    ITEMS_PER_PAGE = 20


class DevelopmentConfig(Config):
    DEBUG = True
    

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
