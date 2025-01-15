# In models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # This is fine; it will be initialized with the app later

# Import models after db initialization
from .user import User
from .transaction import Transaction

# Import your models here
from .category import Category
from .product import Product
from .cart import Cart
from .cart_item import CartItem
from .order import Order
from .payment import Payment
from .user_item import UserItem

# Export your models to make them accessible
__all__ = ["db", "Product", "Category", "User", "Cart", "CartItem", "Order", "Payment", "UserItem","transaction"]
