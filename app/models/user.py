from .. import db
from datetime import datetime
from flask_login import UserMixin
from app.utils.aes import AESCipher

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reviews = db.relationship('Review', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        cipher = AESCipher()
        self.password = cipher.encrypt_password(password)  # Diubah menjadi encrypt_password

    def check_password(self, password):
        try:
            cipher = AESCipher()
            decrypted = cipher.decrypt_password(self.password)  # Diubah menjadi decrypt_password
            return decrypted == password
        except Exception as e:
            print(f"Password check error: {e}")
            return False
        
    def check_admin(self):  # Ubah is_admin menjadi check_admin
        return self.role == 'admin'