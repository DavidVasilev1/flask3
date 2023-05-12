from flask import Blueprint, render_template, redirect, url_for, request, jsonify, make_response
from flask_login import login_required, logout_user, login_user
from functools import wraps
import jwt
from nighthawkguessr_api.model.user import User
from http import cookies
import bcrypt
from bcrypt import gensalt
from nighthawkguessr_api.forms import RegisterForm, LoginForm
from nighthawkguessr_api.model.user import db
from flask import current_app

jwt_bp = Blueprint('jwt_auth', __name__)



def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       # Grabs the cookie from request  headers
       cookieString = request.headers.get('Cookie')
       # loads the cookie into cookie object
       if cookieString:
           cookie = cookies.SimpleCookie()
           cookie.load(cookieString)
            # if token exist then it grabs the token from the cookie
           if 'token' in cookie:
               token = cookie['token'].value
 
        # if no token exits it shows a message saying valid token is missing 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
        # this code tries to verify the signature of the token by decoding it.
       try:
           data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(username=data['name']).first()
        # if signature is not valid or it is not able to decode it writes a message saying token is invalid. 
       except:
           return jsonify({'message': 'token is invalid'})
        # returns current user
       return f(current_user, *args, **kwargs)
       # returns the decorator
   return decorator

from flask import request
@jwt_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username or password field is empty.'}), 400

    user = User.query.filter_by(username=data.get('username')).first()

    if user:
        return jsonify({'message': 'User already exists. Please Log in.'}), 400

    hashed_password = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # ensure the hashed password is in string format

    new_user = User(username=data.get('username'), password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'}), 201


@jwt_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and bcrypt.checkpw(data.get('password').encode('utf-8'), user.password.encode('utf-8')):
        token = jwt.encode(payload= {'name': user.username}, key=current_app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token}), 200  # 200 is a typical HTTP status code for a successful request
    return jsonify({'message': 'Invalid username or password'}), 401  # 401 is a typical HTTP status code for unauthorized access


@jwt_bp.route('/dashboard', methods=['GET', 'POST'])
@token_required
def dashboard(temp):
    return render_template('index.html')
# This redirects to dashboard page ones loged in, and log in succesful is required.

@jwt_bp.route('/logout', methods=['GET', 'POST'])
@token_required
def logout(temp):
    logout_user()
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', expires=0)
    return response

