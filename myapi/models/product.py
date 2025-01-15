from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from myapi.models import db

import json

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    media = db.Column(db.Text, nullable=True)  # Store media as JSON string
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    designer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    meta = db.Column(db.Text, nullable=True)  # Store meta as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    designer = db.relationship('User', backref=db.backref('designed_products', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'short_description': self.description[:150],
            'price': self.price,
            'image': self.image,
            'media': json.loads(self.media) if self.media else {},
            'category_id': self.category_id,
            'designer_id': self.designer_id,
            'meta': json.loads(self.meta) if self.meta else {},
            'created_at': self.created_at.isoformat()
        }

    def from_dict(self, data):
        for field in ['title', 'description', 'price', 'image', 'media', 'category_id', 'designer_id', 'meta']:
            if field in data:
                setattr(self, field, data[field] if field not in ['meta', 'media'] else json.dumps(data[field]))