from flask import render_template, request, jsonify
from flask_login import current_user
from . import main_bp
from app import db
from app.models.restaurant import Restaurant

@main_bp.route('/')
def home():
    restaurants = Restaurant.query.order_by(Restaurant.rating_average.desc()).limit(6).all()
    return render_template('home.html', restaurants=restaurants)

@main_bp.route('/restaurants')
def list_restaurants():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Restaurant.query
    
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Restaurant.name.ilike(f'%{search}%'))
    
    restaurants = query.paginate(page=page, per_page=12)
    return render_template('user/restaurants.html', 
                     restaurants=restaurants,
                     is_admin=current_user.check_admin() if not current_user.is_anonymous else False)

@main_bp.route('/restaurant/<int:id>')
def restaurant_detail(id):
    restaurant = Restaurant.query.get_or_404(id)
    return render_template('user/restaurant_detail.html', 
                         restaurant=restaurant,
                         is_admin=current_user.check_admin() if not current_user.is_anonymous else False)