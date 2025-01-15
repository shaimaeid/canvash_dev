from flask import request, jsonify
from myapi.models import db, User
from myapi.services.cart_service import CartService
from werkzeug.security import generate_password_hash, check_password_hash
from myapi.routes.api import api
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful', 'user': user.to_dict()})
    return jsonify({'message': 'Invalid credentials'}), 401


@api.route('/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})


@api.route('/users', methods=['GET'])
def all_users():
    users = User.query.all()
    users = [user.to_dict() for user in users]
    return jsonify(users)

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict())

@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if data.get('password'):
        user.password = generate_password_hash(data['password'], method='sha256')

    db.session.commit()

    return jsonify(user.to_dict())

@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

@api.route('/user/<int:id>/cart', methods=['POST'])
def add_to_cart(id):
    data = request.get_json()
    # set default user id =2 if no user_id sent
    user_id = id or 2
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    cart_item = CartService.add_to_cart(user_id, product_id, quantity)
    if not cart_item:
        return jsonify({'error': 'Could not add item to cart'}), 400
    return jsonify(cart_item.to_dict()), 201