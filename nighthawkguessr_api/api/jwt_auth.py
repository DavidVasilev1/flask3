from flask import Blueprint, render_template, redirect, url_for, request, jsonify, make_response
from flask_login import login_required, logout_user, login_user
from functools import wraps
import jwt
from nighthawkguessr_api.model.user import User
from http import cookies
import bcrypt
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

@jwt_bp.route('/register', methods=['GET', 'POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
       hashed_password = bcrypt.generate_password_hash(form.password.data)
       new_user = User(username=form.username.data, password=hashed_password)
       db.session.add(new_user)
       db.session.commit()
       return redirect(url_for('login'))


   return render_template('register.html', form=form)

@jwt_bp.route('/login', methods=['GET', 'POST'])
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
                token = jwt.encode(payload= {'name': user.username}, key=current_app.config['SECRET_KEY'], algorithm="HS256")
                # calls for dashboad url
                response = make_response(redirect(url_for('dashboard')))
                # sets the token in a cookie
                response.set_cookie('token', token) 
                # return response back to client 
                return response
        # if validation is not succesful it goes back to log in page
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@jwt_bp.route('/dashboard', methods=['GET', 'POST'])
@token_required
def dashboard(temp):
    return render_template('dashboard.html')
# This redirects to dashboard page ones loged in, and log in succesful is required.

@jwt_bp.route('/logout', methods=['GET', 'POST'])
@token_required
def logout(temp):
    logout_user()
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', expires=0)
    return response

