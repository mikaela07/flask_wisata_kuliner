import os
from datetime import timedelta
from dotenv import load_dotenv
import pymysql


pymysql.install_as_MySQLdb()
load_dotenv()

class Config:
   SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
   
   # Database
   SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:@localhost/wisata_kuliner')
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   
   # Upload
   UPLOAD_FOLDER = 'static/uploads'
   MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
   
   # Session
   PERMANENT_SESSION_LIFETIME = timedelta(days=7)
   SESSION_COOKIE_SECURE = True
   REMEMBER_COOKIE_SECURE = True
   SESSION_COOKIE_HTTPONLY = True 
   REMEMBER_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
   DEBUG = True
   SESSION_COOKIE_SECURE = False
   REMEMBER_COOKIE_SECURE = False

class ProductionConfig(Config):
   DEBUG = False
   SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL')

class TestingConfig(Config):
   TESTING = True
   SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
   WTF_CSRF_ENABLED = False

config = {
   'development': DevelopmentConfig,
   'production': ProductionConfig, 
   'testing': TestingConfig,
   'default': DevelopmentConfig
}

# class Config:
#     SECRET_KEY = 'your-secret-key'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/wisata_kuliner'

# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/wisata_kuliner'

# config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }