from flask import Flask, render_template, url_for, redirect, Blueprint, request, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
import random
import requests
import string
import json 
import http.cookies as cookies
  
from model.auth import User, token_required


jwt_api = Blueprint('pass_api', __name__, url_prefix='/api/pass')

api = Api(jwt_api)


@app.route('/generate_password', methods=['GET'])
def getPassAPI(length=3):
  password = []
  url = "https://random-words5.p.rapidapi.com/getMultipleRandom"
  querystring = {"count": str(length)}
  headers = {
      "X-RapidAPI-Key": "f0aeb431bamshc18b522b64e7383p102f67jsnea4673acfc55",
      "X-RapidAPI-Host": "random-words5.p.rapidapi.com"
  }
  response = requests.request("GET", url, headers=headers, params=querystring)
  words = response.json()
  password += words
  num_random_chars = (length * 2) - len(words)
  password += [random.choice(string.ascii_letters + string.digits) for i in range(num_random_chars)]
  random.shuffle(password)
  response = ''.join(password)
  return response




@app.route('/generate_random_password')
def index():
  password = getPassAPI(5)  # generate password of length 5
  save_to_json(password)
  return render_template('genpass.html', password=password)


class PassAPI:
  class _Read(Resource):
      def get(self):
          return getPassAPI()

  api.add_resource(_Read, '/')


def save_to_json(password):
  # open the JSON file in write mode
  with open('passwords.json', 'w') as f:
      # write the password to the file as a JSON object
      json.dump({"password": password}, f)



@ app.route('/register', methods=['GET', 'POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
       hashed_password = bcrypt.generate_password_hash(form.password.data)
       new_user = User(username=form.username.data, password=hashed_password)
       db.session.add(new_user)
       db.session.commit()
       return redirect(url_for('login'))


   return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    # loads login form
    form = LoginForm()
    # when user submits information it creates a token (this is where a token is created and stored in a cookie)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # checks the user entered password against the database stored password
            if bcrypt.check_password_hash(user.password, form.password.data):
                # This is were token is created . Takes the payload with username and encodes using the secret key and algorithm(HS256).
                token = jwt.encode(payload= {'name': user.username}, key=app.config['SECRET_KEY'], algorithm="HS256")
                # calls for dashboad url
                response = make_response(redirect(url_for('dashboard')))
                # sets the token in a cookie
                response.set_cookie('token', token) 
                # return response back to client 
                return response
        # if validation is not succesful it goes back to log in page
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)












@app.route('/dashboard', methods=['GET', 'POST'])
#token required to access this page, ONLY once token is validated this page can be accesed at all times. 
@token_required
def dashboard(temp):
    return render_template('dashboard.html')
# This redirects to dashboard page ones loged in, and log in succesful is required.

@app.route('/logout', methods=['GET', 'POST'])
@token_required
def logout(temp):
    logout_user()
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', expires=0)
    return response

# Logout and redirects you back to log in
# call the function to save the password to the JSON file

save_to_json(getPassAPI(7))  # generate password of length 7
