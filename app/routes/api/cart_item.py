from flask import Blueprint, request, jsonify
from app.models import db, CartItem
from app.routes.api import api

@api.route('/cart_items', methods=['POST'])
def create_cart_item():
    data = request.get_json()
    cart_id = data.get('cart_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not cart_id or not product_id:
        return jsonify({'error': 'Missing required fields'}), 400

    new_cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)

    db.session.add(new_cart_item)
    db.session.commit()

    return jsonify(new_cart_item.to_dict()), 201

@api.route('/cart_items/<int:id>', methods=['GET'])
def get_cart_item(id):
    cart_item = CartItem.query.get(id)
    if not cart_item:
        return jsonify({'error': 'CartItem not found'}), 404

    return jsonify(cart_item.to_dict())

@api.route('/cart_items/<int:id>', methods=['PUT'])
def update_cart_item(id):
    cart_item = CartItem.query.get(id)
    if not cart_item:
        return jsonify({'error': 'CartItem not found'}), 404

    data = request.get_json()
    cart_item.cart_id = data.get('cart_id', cart_item.cart_id)
    cart_item.product_id = data.get('product_id', cart_item.product_id)
    cart_item.quantity = data.get('quantity', cart_item.quantity)

    db.session.commit()

    return jsonify(cart_item.to_dict())

@api.route('/cart_items/<int:id>', methods=['DELETE'])
def delete_cart_item(id):
    cart_item = CartItem.query.get(id)
    if not cart_item:
        return jsonify({'error': 'CartItem not found'}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({'message': 'CartItem deleted successfully'}), 200