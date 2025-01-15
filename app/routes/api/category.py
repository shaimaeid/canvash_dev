from flask import Blueprint, request, jsonify
from app.models import db, Category
from app.routes.api import api

@api.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    
    return jsonify([category.to_dict() for category in categories])

@api.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    slug = data.get('slug')
    icon = data.get('icon')

    if not name or not slug:
        return jsonify({'error': 'Missing required fields'}), 400

    new_category = Category(name=name, description=description, slug=slug, icon=icon)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(new_category.to_dict()), 201

@api.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify(category.to_dict())

@api.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    data = request.get_json()
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    category.slug = data.get('slug', category.slug)
    category.icon = data.get('icon', category.icon)

    db.session.commit()

    return jsonify(category.to_dict())

@api.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': 'Category deleted successfully'}), 200