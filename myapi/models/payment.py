from datetime import datetime
from myapi.models import db


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    transaction_id = db.Column(db.String(50), nullable=False, unique=True)
    payment_method = db.Column(db.String(20), nullable=False)  # e.g., 'gumroad'
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='USD')
    payment_status = db.Column(db.String(20), nullable=False, default='pending')  # e.g., 'pending', 'successful', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Backreference to Order
    order = db.relationship('Order', backref=db.backref('payment', uselist=False))
