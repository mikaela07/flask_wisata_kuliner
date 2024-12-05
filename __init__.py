# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from config import config

# db = SQLAlchemy()
# login_manager = LoginManager()

# def create_app(config_name):
#     app = Flask(__name__)
    
#     # Load config
#     app.config.from_object(config[config_name])
    
#     # Initialize extensions
#     db.init_app(app)
#     login_manager.init_app(app)
#     login_manager.login_view = 'auth.login'
    
#     # Register blueprints
#     from .auth import auth_bp # type: ignore
#     app.register_blueprint(auth_bp)
    
#     # other blueprints...
    
#     return app