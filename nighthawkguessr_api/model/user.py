from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt
from nighthawkguessr_api import db


# database
class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), nullable=False, unique=True)
   password = db.Column(db.String(80), nullable=False)


# The check_password function is a method of the User class.
# It's used to verify if the provided password matches the hashed password stored in the database.
   def check_password(self, password):
       return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
