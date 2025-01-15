from app.routes.web import web
from flask import request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from app.models import db, Product, User, Cart, CartItem, Category
from app.logger import mylogger
from flask_login import current_user

bcrypt = Bcrypt()

@web.route('/user/login', methods=['GET', 'POST'])
def web_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('web.get_user'))
        flash('Invalid credentials', 'danger')
    return render_template('user/login.html')

@web.route('/user/logout', methods=['GET'])
@login_required
def web_logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('web.web_login'))

@web.route('/users', methods=['GET'])
def get_users():
    
    return render_template('index.html') 

@web.route('/user', methods=['GET'])
@login_required
def get_user():
    
    return render_template('user/profile.html') 

@web.route('/user/cart', methods=['GET'])
def get_user_cart():
    if not current_user.is_authenticated:
        return redirect(url_for('web.web_login'))
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        return render_template('pages/404.html'), 404

    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    products = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        product.quantity = item.quantity  # Add quantity attribute to product
        products.append(product)

    sub_total = sum([product.price * product.quantity for product in products])
    service = round(sub_total * 0.1)
    total = sub_total + service
    mylogger.debug('products: %s', products)
    print('products:', products)
    return render_template('product/cart.html', products=products, total=total, service=service)