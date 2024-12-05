from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from ..models.user import User
from .. import db

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validasi data tidak kosong
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        # Buat user baru dengan password yang dienkripsi
        user = User(username=username, email=email, password=password)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return redirect(url_for('auth.login'))
        
        try:
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):  # Perubahan di sini
                login_user(user)
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('main.home'))
                
            flash('Invalid username or password', 'error')
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
        
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return render_template('auth/login.html')