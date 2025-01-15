from datetime import datetime
from myapi.models import db


class UserItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    downloads = db.Column(db.Integer, default=0)
    rating = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='user_items', lazy=True)
    product = db.relationship('Product', backref='user_items', lazy=True)
    order = db.relationship('Order', backref='user_items', lazy=True)

    def __repr__(self):
        return f'<UserItem {self.product_id} - {self.order_id}>'
