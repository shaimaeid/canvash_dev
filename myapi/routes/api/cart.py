from flask import Blueprint, request, jsonify
from myapi.services.cart_service import CartService
from myapi.routes.api import api

@api.route('/carts', methods=['POST'])
def create_cart():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing required fields'}), 400

    new_cart = CartService.create_cart(user_id)
    return jsonify(new_cart.to_dict()), 201

@api.route('/carts', methods=['GET'])
def get_carts():
    carts = CartService.get_all_carts()
    return jsonify([cart.to_dict() for cart in carts])

@api.route('/carts/<int:id>', methods=['GET'])
def get_cart(id):
    cart = CartService.get_cart_by_id(id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    return jsonify(cart.to_dict())

@api.route('/carts/<int:id>', methods=['PUT'])
def update_cart(id):
    data = request.get_json()
    user_id = data.get('user_id')

    cart = CartService.update_cart(id, user_id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    return jsonify(cart.to_dict())

@api.route('/carts/<int:id>', methods=['DELETE'])
def delete_cart(id):
    cart = CartService.delete_cart(id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    return jsonify({'message': 'Cart deleted successfully'}), 200

