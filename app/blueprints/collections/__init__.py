from flask import Blueprint

collections_bp = Blueprint('collections_bp', __name__)

from . import routes