from flask import Blueprint ,jsonify , request

from app.extensions import db
from app.models.user import Users
from app.models.database import Dataset
from app.models.eda_report import EDAReport

user_bp = Blueprint('user' , __name__)

@user_bp.get('/overview')
def overview():
    return jsonify({'message':"This is overview api"})