from .. import db
from datetime import datetime

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    address = db.Column(db.String(200))
    rating_average = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', backref='restaurant', lazy=True)
    favorites = db.relationship('Favorite', backref='restaurant', lazy=True)

    def __init__(self, name, category, description=None, address=None):
        self.name = name
        self.category = category
        self.description = description
        self.address = address

    def update_rating_average(self):
        if self.reviews:
            total_rating = sum(review.rating for review in self.reviews)
            self.rating_average = total_rating / len(self.reviews)
        else:
            self.rating_average = 0.0