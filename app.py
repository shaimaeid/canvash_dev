import os
from flask import Flask
from dotenv import load_dotenv
from app.routes.web import web
from app.routes.api import api
from app.models import db
from flask_migrate import Migrate
from app.auth import login_manager
from flask_login import current_user
import paypalrestsdk
import paypal_config

# Context processor to inject current user and cart count into templates
@web.context_processor
def inject_user():
    active_cart = current_user.active_cart() if current_user.is_authenticated else None
    cart_count = active_cart.cart_count() if active_cart else 0
    return {'current_user': current_user , 'cart_count': cart_count}

# Application factory to create the Flask app
def create_app(test_config=None):
    load_dotenv()  # Load environment variables from .env file
    
    app = Flask(__name__)

    # Default configurations
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Apply test configurations if provided
    if test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite for testing
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(basedir, 'database', 'app.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)  # Initialize Flask-Login manager
    login_manager.login_view = 'web.web_login'  # Define the login view

    migrate = Migrate(app, db)

    # Register blueprints (web and api routes)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(web)

    return app


# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # Get host and port from environment variables, default to '127.0.0.1' and '5000' respectively
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    
    # Run the Flask app with the specified host and port
    app.run(
        host=host,
        port=port,
        debug=True  # Set to False in production
    )
