
from flask import redirect, url_for
from flask_login import LoginManager
from myapi.models import User

login_manager = LoginManager()

# User loader function
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect to a special page for unauthorized access."""
    return redirect(url_for('web.unauthorized_access'))

# Ensure you have a route for 'unauthorized_access' in your web blueprint