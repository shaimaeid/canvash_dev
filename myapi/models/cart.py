import enum
from datetime import datetime, timedelta
from myapi.models import db


class CartStatus(enum.IntEnum):
    ACTIVE = 1
    CONVERTED = 2
    ABANDONED = 3
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    status = db.Column(db.Integer, nullable=False, default=CartStatus.ACTIVE)
    items = db.relationship('CartItem', backref='cart', lazy=True)

    @property
    def status_enum(self):
        return CartStatus(self.status)

    @status_enum.setter
    def status_enum(self, status):
        self.status = status.value
    
    def is_abandoned(self, time_limit=timedelta(days=7)):
        """Check if the cart is abandoned."""
        return self.status_enum == CartStatus.ACTIVE and self.updated_at < datetime.utcnow() - time_limit
    
    def cart_count(self):
        return sum(cart_item.quantity for cart_item in self.items)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }