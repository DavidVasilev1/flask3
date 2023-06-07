from flask import Blueprint, render_template, redirect, url_for, request, jsonify, make_response
from functools import wraps
from http import cookies
import bcrypt
from bcrypt import gensalt
from nighthawkguessr_api.model.user import db
from flask import current_app
from nighthawkguessr_api import app, db, project_path
from datetime import datetime, timedelta
from nighthawkguessr_api.model.user import User, db
from flask_jwt import jwt_required, current_identity


jwt_bp = Blueprint('jwt_auth', __name__)
# Creating a blueprint for jwt_auth related routes

def authenticate(username, password):
    user = User.query.filter_by(username=username).one_or_none()
    if not user:
        return None

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).one_or_none()

@jwt_bp.route('/auth_status', methods=['GET'])
@jwt_required()
def auth_status():
    return jsonify({'username': current_identity.username})

@jwt_bp.route('/register', methods=['POST'])
def register():
   data = request.get_json()
   if not data or not data.get('username') or not data.get('password'):
       return jsonify({'message': 'Username or password field is empty.'}), 400
   user = User.query.filter_by(username=data.get('username')).first()
   if user:
       return jsonify({'message': 'User already exists. Please Log in.'}), 400


   hashed_password = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt()) 
   new_user = User(username=data.get('username'), password=hashed_password)
   db.session.add(new_user)
   db.session.commit()
   return jsonify({'message': 'New user created!'}), 201

""" 
@jwt_bp.route('/login', methods=['POST'])
def login():
   data = request.get_json()
   username = data.get('username')
   password = data.get('password')

   user = User.query.filter_by(username=username).first()

   if user is None or not user.check_password(password):
       return jsonify({'message': 'Invalid username or password'}), 400

   token = jwt.encode(payload= {'name': user.username}, key=current_app.config['SECRET_KEY'], algorithm="HS256")
   print("Token:", token)

   expires = datetime.now()
   expires = expires + timedelta(days=30) 
   response = make_response(jsonify({'message': 'Logged in'}), 200)
   response.set_cookie('token', token, secure=True, samesite='None', path='/', httponly=True)
  
   print(response.headers)
   return response
"""