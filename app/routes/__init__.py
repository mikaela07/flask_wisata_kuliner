# File ini untuk menginisialisasi blueprint
from flask import Blueprint

# Buat blueprint untuk setiap modul
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)
user_bp = Blueprint('user', __name__, url_prefix='/user')

