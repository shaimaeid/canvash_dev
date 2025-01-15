import random
from app import create_app
from myapi.models import db, Product, Category, User, Cart, CartItem
from myapi.logger import mylogger
from flask_login import current_user, login_user
from flask import request

# Create app instance
app = create_app()

# Create both application and request contexts
with app.app_context():
    with app.test_request_context():
        # Get user with ID 4 using modern SQLAlchemy syntax
        user = db.session.get(User, 4)
        if user:
            login_user(user)
            print(f"Logged in user: {current_user}")
            print(f"User ID: {current_user.id}")
            print(f"Username: {current_user.username}")
            print(f"Email: {current_user.email}")
        else:
            print("User with ID 4 not found")
