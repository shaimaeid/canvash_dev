from flask import jsonify, request, render_template, Blueprint
from app.routes.web import web
from app.models import db, Product, User, Cart, CartItem, Category
from app.routes.api import api
from app.logger import mylogger

@web.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    products_pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    products = products_pagination.items
    
    return render_template('product/products.html', products=products,total=len(products), pagination=products_pagination)

@web.route('/category/<string:slug>', methods=['GET'])
def get_category_products(slug):
    page = request.args.get('page', 1, type=int)
    per_page = 6
    category = Category.query.filter_by(slug=slug).first()
    # Check if category exists and return 404 if not
    if category is None:
        # use the 404 error handler
        return render_template('pages/404.html'), 404
    
    products_pagination = Product.query.filter_by(category_id=category.id).paginate(page=page, per_page=per_page, error_out=False)
    products = products_pagination.items
   
    return render_template('product/category.html', category=category, products=products, pagination=products_pagination)

@web.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return render_template('product/product.html', product=product)

