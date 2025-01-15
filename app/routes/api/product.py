# product.py
from flask import Blueprint, request, jsonify
from myapi.models import db, Product
from myapi.logger import mylogger
from werkzeug.utils import secure_filename
import os
from myapi.routes.api import api


@api.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product()
    product.from_dict(data)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@api.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    
    return jsonify([product.to_dict() for product in products])

@api.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict())

@api.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.get_json()
    product.from_dict(data)
    db.session.commit()
    return jsonify(product.to_dict())

@api.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

@api.route('/upload_image', methods=['POST'])
def upload_image():
    mylogger.info("accessed")
    file_path = "myapi/static/user_files/"
    
    if 'image' in request.files:
        file = request.files['image']
        filename = secure_filename(file.filename)
        mylogger.info(filename)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        mylogger.info(file_path+filename)
        file.save(os.path.join(file_path, filename))
        return jsonify({"message": "Image uploaded successfully", "filename": filename}), 201

    return jsonify({"error": "No file uploaded"}), 400