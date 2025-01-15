from datetime import datetime
from enum import Enum
from . import db

class TransactionSource(Enum):
    PAYPAL = "paypal"
    STRIPE = "stripe"
    GUMROAD = "gumroad"
    CASH = "cash"

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)  # ISO 4217 currency codes
    method = db.Column(db.Enum(TransactionSource), nullable=False)  # Updated field
    status = db.Column(db.Enum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)
    reference_id = db.Column(db.String(50), nullable=True, index=True)  # Unique ID from payment gateway
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='transactions')

    def complete_transaction(self):
        """Mark transaction as completed and update user balance."""
        if self.status != TransactionStatus.COMPLETED:
            self.status = TransactionStatus.COMPLETED
            self.user.balance += self.amount if self.method == TransactionSource.CASH else -self.amount
            db.session.commit()
    
    def to_dict(self):
        """Convert transaction to dictionary for easy serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "currency": self.currency,
            "method": self.method.value,
            "status": self.status.value,
            "reference_id": self.reference_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def __repr__(self):
        return f"<Transaction {self.id}>"