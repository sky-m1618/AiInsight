from flask import Blueprint , request ,jsonify
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import Users

auth_bp = Blueprint('auth',__name__)

@auth_bp.post('/login')
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(username = username).first()
    if not user:
        return jsonify( {'message': "Invalid Username"}),404
    if not user.check_password(password):
        return jsonify({'message':'Invalid password'} ),404
    if user.role == 'ADMIN':
        token = create_access_token(identity=user.id , additional_claims={'role':'ADMIN'})
        return jsonify({'token':token , 'admin':user.to_dict()}),200
    else:
        token = create_access_token(identity=user.id , additional_claims={'role':'USER'})
        return jsonify({'token':token , 'user':user.to_dict()}),200



@auth_bp.post('user/register')
def register():
    data = request.get_json(force=True)

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')


    user = Users.query.filter_by(username = username).first()
    if user:
        return jsonify({'message':'Username already exists'}),400

    user = Users.query.filter_by(email = email).first()

    if user:
        return jsonify({'message':'Email already exists'}),400


    new_user = Users(
        username=username,
        email = email,
    )
    new_user.set_password(password)

    db.session.add()
    db.session.commit()
    user = Users.query.filter_by(username = username).first()
    token = create_access_token(identity=user.id , additional_claims=({'role':'USER'}))
    return jsonify({'message':'Registration successfull.....' , 'token':token , 'user':user.to_dict()}),200
