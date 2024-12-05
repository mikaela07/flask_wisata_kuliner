from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from . import admin_bp
from app.models import User, Restaurant, Review, db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.check_admin():
            flash('Access denied', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_restaurants = Restaurant.query.count()
    total_reviews = Review.query.count()
    
    # Calculate average rating and handle None case
    avg_rating = 0.0
    if total_reviews > 0:
        reviews = Review.query.with_entities(Review.rating).all()
        avg_rating = float(sum(review[0] for review in reviews)) / total_reviews
    
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_restaurants=total_restaurants,
                         total_reviews=total_reviews,
                         avg_rating=avg_rating,
                         recent_reviews=recent_reviews,
                         recent_users=recent_users)

@admin_bp.route('/restaurants')
@login_required
@admin_required
def manage_restaurants():
    restaurants = Restaurant.query.all()
    return render_template('admin/manage_restaurants.html', restaurants=restaurants)

@admin_bp.route('/restaurant/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_restaurant():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        address = request.form.get('address')

        if not name or not category:
            flash('Name and category are required', 'error')
            return redirect(url_for('admin.add_restaurant'))

        try:
            restaurant = Restaurant(
                name=name,
                category=category, 
                description=description,
                address=address
            )
            db.session.add(restaurant)
            db.session.commit()
            flash('Restaurant added successfully', 'success')
            return redirect(url_for('admin.manage_restaurants'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding restaurant: {str(e)}', 'error')
            return redirect(url_for('admin.add_restaurant'))
    
    return render_template('admin/add_restaurant.html')

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/restaurant/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    if request.method == 'POST':
        restaurant.name = request.form['name']
        restaurant.category = request.form['category']
        restaurant.description = request.form['description']
        restaurant.address = request.form['address']
        
        db.session.commit()
        flash('Restaurant updated successfully', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/edit_restaurant.html', restaurant=restaurant)