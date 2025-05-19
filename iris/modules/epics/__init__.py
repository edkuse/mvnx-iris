from flask import Blueprint

bp = Blueprint('epics', __name__, template_folder='templates', url_prefix='/epics')

from . import routes
