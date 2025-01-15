from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import backref
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    ADMIN = 'admin'
    SUBSCRIBER = 'subscriber'
    DESIGNER = 'designer'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, nullable=True, default=0.0)
    role = db.Column(db.String(20), nullable=False, default=SUBSCRIBER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    carts = db.relationship('Cart', backref=backref('user_owner', lazy=True))
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def active_cart(self):
        return max(self.carts, key=lambda c: c.created_at) if self.carts else None
    
    def cart_count(self):
        return sum([cart.cart_count() for cart in self.carts])
    
    def can_afford(self, amount):
        return self.balance >= amount
     
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'balance': self.balance,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'