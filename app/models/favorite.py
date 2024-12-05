from app.models import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    restaurant = db.relationship('Restaurant', backref=db.backref('favorited_by', lazy=True))