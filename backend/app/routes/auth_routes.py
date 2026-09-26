from flask import Blueprint
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import Users

auth_bp = Blueprint('auth',__name__)