from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os

"""
These object can be used throughout project.
1.) Objects from this file can be included in many blueprints
2.) Isolating these object definitions avoids duplication and circular dependencies
"""

# Setup of key Flask object (app)
app = Flask(__name__)
project_path = Path.cwd().as_posix()
# Setup SQLAlchemy object and properties for the database (db)
file_path = os.path.abspath(os.getcwd())+"/nighthawkguessr_api/volumes/sqlite.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'+file_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "SECRET_KEY"
db = SQLAlchemy(app)

# Images storage
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # maximum size of uploaded content
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".gif"]  # supported file types
app.config["UPLOAD_FOLDER"] = "volumes/uploads/"  # location of user uploaded content
