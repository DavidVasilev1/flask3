from datetime import datetime, timedelta
from flask import Blueprint, current_app, jsonify, make_response, request
from flask_login import login_required, logout_user, login_user
from functools import wraps
from http import cookies
from nighthawkguessr_api import app, db, project_path
from nighthawkguessr_api.model.user import User
import bcrypt
import jwt

jwt_bp = Blueprint('jwt_auth', __name__)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        cookieString = request.headers.get('Cookie')

        if cookieString:
            cookie = cookies.SimpleCookie()
            cookie.load(cookieString)

            if 'token' in cookie:
                token = cookie['token'].value

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['name']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


@jwt_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username or password field is empty.'}), 400

    user = User.query.filter_by(username=data.get('username')).first()

    if user:
        return jsonify({'message': 'User already exists. Please Log in.'}), 400
 
    hashed_password = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=data.get('username'), password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'}), 201


@jwt_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 400

    token = jwt.encode(payload= {'name': user.username}, key=current_app.config['SECRET_KEY'], algorithm="HS256")

    expires = datetime.now()
    expires = expires + timedelta(days=30)

    response = make_response(jsonify({'message': 'Logged in'}), 200)
    response.set_cookie('token', token, secure=True, samesite='None', path='/')

    return response



