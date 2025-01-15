from flask import Blueprint

api = Blueprint('api', __name__)

from myapi.routes.api import product, user, cart, cart_item, category, payment
