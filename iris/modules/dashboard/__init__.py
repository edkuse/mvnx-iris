from flask import Blueprint

bp = Blueprint('dashboard', __name__, template_folder='templates', url_prefix='/')

from . import routes
