# conftest.py
import pytest
from src.app import create_app
from src.myapi.models import db

@pytest.fixture(scope='module')
def app():
    # Create a Flask app instance for testing with a test-specific configuration
    app = create_app(test_config=True)
    
    # Ensure the app context is pushed
    with app.app_context():
        # Initialize the database
        db.create_all()  # Create tables for testing
        yield app  # This will be passed to each test as the 'app' fixture
        
        # After all tests, drop the test database
        db.session.remove()
        db.drop_all()

    return app

@pytest.fixture(scope='module')
def client(app):
    # Create and return a test client
    return app.test_client()
