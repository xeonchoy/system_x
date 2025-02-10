from flask import Blueprint
from .register import register_routes
from .login import login_routes

auth_bp = Blueprint('auth', __name__)

# Register routes from both modules
register_routes(auth_bp)
login_routes(auth_bp)
