from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import user_bp
from app.models.review import Review, Favorite
from app.models.restaurant import Restaurant
from app.models import db

@user_bp.route('/profile')
@login_required
def profile():
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    recent_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).limit(5).all()
    
    # Calculate average rating
    ratings_avg = 0.0
    if reviews:
        ratings_avg = sum(review.rating for review in reviews) / len(reviews)
    
    return render_template('user/profile.html',
                         reviews=reviews,
                         favorites=favorites,
                         recent_reviews=recent_reviews,
                         ratings_avg=ratings_avg)

@user_bp.route('/reviews')
@login_required
def my_reviews():
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    return render_template('user/reviews.html', reviews=reviews)

@user_bp.route('/review/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    if review.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('user.my_reviews'))
    
    if request.method == 'POST':
        try:
            rating = int(request.form.get('rating', 0))  # Gunakan 0 sebagai default
            comment = request.form.get('comment', '')
            
            # Validasi rating
            if not isinstance(rating, int) or not 1 <= rating <= 5:
                flash('Rating harus antara 1-5', 'error')
                return redirect(url_for('user.edit_review', review_id=review_id))
            
            # Update review
            review.rating = rating
            review.comment = comment
            db.session.commit()
            
            # Update rating restoran
            restaurant = Restaurant.query.get(review.restaurant_id)
            restaurant.update_rating_average()
            db.session.commit()
            
            flash('Review berhasil diperbarui', 'success')
            return redirect(url_for('user.my_reviews'))
            
        except (ValueError, TypeError) as e:
            flash('Rating tidak valid', 'error')
            return redirect(url_for('user.edit_review', review_id=review_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating review: {str(e)}', 'error')
            return redirect(url_for('user.edit_review', review_id=review_id))
            
    return render_template('user/edit_review.html', review=review)

@user_bp.route('/favorites')
@login_required
def my_favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('user/favorites.html', favorites=favorites)

@user_bp.route('/review/add/<int:restaurant_id>', methods=['POST'])
@login_required
def add_review(restaurant_id):
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    
    if not 1 <= rating <= 5:
        flash('Invalid rating', 'error')
        return redirect(url_for('main.restaurant_detail', id=restaurant_id))
    
    review = Review(
        user_id=current_user.id,
        restaurant_id=restaurant_id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(review)
    db.session.commit()
    
    # Update restaurant rating
    restaurant = Restaurant.query.get(restaurant_id)
    restaurant.update_rating_average()
    db.session.commit()
    
    flash('Review added successfully', 'success')
    return redirect(url_for('main.restaurant_detail', id=restaurant_id))

@user_bp.route('/review/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    if review.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('user.my_reviews'))
    
    try:
        restaurant_id = review.restaurant_id
        db.session.delete(review)
        db.session.commit()
        
        # Update rating restoran
        restaurant = Restaurant.query.get(restaurant_id)
        restaurant.update_rating_average()
        db.session.commit()
        
        flash('Review deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting review', 'error')
    
    return redirect(url_for('user.my_reviews'))

@user_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not username or not email:
        flash('Username and email are required', 'error')
        return redirect(url_for('user.profile'))
    
    # Validasi format email sederhana
    if '@' not in email or '.' not in email:
        flash('Invalid email format', 'error')
        return redirect(url_for('user.profile'))
    
    # Update password jika ada
    if new_password:
        if new_password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('user.profile'))
            
        try:
            current_user.set_password(new_password)
        except Exception as e:
            print(f"Password update error: {str(e)}")
            flash('Error updating password', 'error')
            return redirect(url_for('user.profile'))
    
    current_user.username = username
    current_user.email = email
    
    try:
        db.session.commit()
        flash('Profile updated successfully', 'success')
    except Exception as e:
        print(f"Database error: {str(e)}")
        db.session.rollback()
        flash('An error occurred while updating profile', 'error')
    
    return redirect(url_for('user.profile'))

from flask import jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user

@user_bp.route('/favorite/toggle/<int:restaurant_id>', methods=['POST'])
@login_required
def toggle_favorite(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        restaurant_id=restaurant_id
    ).first()
    
    try:
        if favorite:
            db.session.delete(favorite)
            is_favorite = False
            message = 'Restaurant removed from favorites'
        else:
            new_favorite = Favorite(
                user_id=current_user.id,
                restaurant_id=restaurant_id
            )
            db.session.add(new_favorite)
            is_favorite = True
            message = 'Restaurant added to favorites'
        
        db.session.commit()
        return jsonify({
            'status': 'success',
            'is_favorite': is_favorite,
            'message': message
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Helper function untuk mengecek status favorite
def is_restaurant_favorite(restaurant_id):
    if not current_user.is_authenticated:
        return False
    return Favorite.query.filter_by(
        user_id=current_user.id,
        restaurant_id=restaurant_id
    ).first() is not None