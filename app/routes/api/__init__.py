from flask import Blueprint

api = Blueprint('api', __name__)

from app.routes.api import product, user, cart, cart_item, category, payment
