from flask import Flask, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
import os
from config import config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf

# Inisialisasi database dan extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()  # Tambahkan ini

def create_app(config_name='default'):
    # Inisialisasi aplikasi Flask
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Load konfigurasi dari config.py
    app.config.from_object(config[config_name])
    
    # Pastikan folder uploads ada
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/wisata_kuliner'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True  # Tambahkan ini
    
    # Inisialisasi extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)  # Tambahkan ini
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from .routes.admin import admin_bp
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.user import user_bp
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    
    # User loader untuk Flask-Login
    from .models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Context processors
    @app.context_processor
    def utility_processor():
        def get_restaurant_categories():
            from .models.restaurant import Restaurant
            return db.session.query(Restaurant.category).distinct().all()
        return dict(categories=get_restaurant_categories)
    
    # Tambahkan context processor untuk CSRF token
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf())
    
    @app.context_processor
    def utility_processor():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf())
    
    # Before request
    @app.before_request
    def before_request():
        g.user = current_user
    
    return app