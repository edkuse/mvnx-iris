from flask import Blueprint

bp = Blueprint('product_ideas', __name__, template_folder='templates', url_prefix='/product-ideas')

from . import routes
