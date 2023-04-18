from flask import Blueprint, render_template, url_for, redirect, request, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

import http.cookies as cookies
from __init__ import db, bcrypt, app

auth = Blueprint('auth', __name__)

login_manager = LoginManager()
# This line creates an instance of the LoginManager class from the flask_login library
login_manager.init_app(app)
# This line initializes the LoginManager instance with your Flask application, app. 
# This is required in order to use the functionality provided by flask_login.


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# The load_user function takes a single argument user_id which is the user's identifier.
# The function returns a user object obtained by querying the User model for the user with the specified user_id. 
# The user object is then stored in the current session,  allowing the application to keep track of the user's identity and state between requests.

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


        
#used to store user information in the database


# This function is to Verify if token is valid, Signature portion of the token
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
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(username=data['name']).first()
        # if signature is not valid or it is not able to decode it writes a message saying token is invalid. 
       except:
           return jsonify({'message': 'token is invalid'})
        # returns current user
       return f(current_user, *args, **kwargs)
       # returns the decorator
   return decorator


# This code is actually a special function. This function will create a custom decorator with the code required to create and validate tokens. Python provides a very amazing feature named function decorators. These function decorators allow very neat features for web development. In Flask, each view is considered as a function, and decorators are used for injecting additional functionality to one or more functions. In this case, the functionality handled by this custom decorator will be to create and validate tokens.



class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    show_password = BooleanField('Show Password')

    submit = SubmitField('Register')


    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'The username already exists. Please choose a different username.')
#This checks if there is already a username in the database and if there is it asks the user to choose a different username

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')












