from flask import Blueprint

web = Blueprint('web', __name__, 
                template_folder='../../templates',
                static_folder='static',
                static_url_path='/static')

from myapi.routes.web import main, product, user