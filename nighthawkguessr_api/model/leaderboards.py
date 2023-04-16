from sqlalchemy import Column, Integer, String, Text
from .. import db
from sqlalchemy.exc import IntegrityError
import json
from werkzeug.security import generate_password_hash, check_password_hash


class Leaderboard(db.Model):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True)
    _username = Column(String(255), unique=True, nullable=False)
    _password = Column(String(255), nullable=False)
    _pointsEasy = Column(Integer, nullable=False)
    _pointsMedium = Column(Integer, nullable=False)
    _pointsHard = Column(Integer, nullable=False)

    def __init__(self, username, password, pointsEasy, pointsMedium, pointsHard):
        self._username = username
        self.set_password(password)
        self._pointsEasy = pointsEasy
        self._pointsMedium = pointsMedium
        self._pointsHard = pointsHard

    def __repr__(self):
        return "<Leaderboard(id='%s', username='%s', pointsEasy='%s', pointsMedium='%s', pointsHard='%s')>" % (
            self.id,
            self.username,
            self.pointsEasy,
            self.pointsMedium,
            self.pointsHard,
        )

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    def is_username(self, username):
        return self._username == username

    @property
    def pointsEasy(self):
        return self._pointsEasy

    @pointsEasy.setter
    def pointsEasy(self, value):
        self._pointsEasy = value

    @property
    def pointsMedium(self):
        return self._pointsMedium

    @pointsMedium.setter
    def pointsMedium(self, value):
        self._pointsMedium = value

    @property
    def pointsHard(self):
        return self._pointsHard

    @pointsHard.setter
    def pointsHard(self, value):
        self._pointsHard = value

    @property
    def password(self):
        return self._password[0:10] + "..."

    def set_password(self, password):
        self._password = generate_password_hash(password, method='sha512')

    def is_password(self, password):
        result = check_password_hash(self._password, password)
        if result:
            return True
        else:
            return False

    def to_dict(self):
        return {"id": self.id, "username": self.username, "password": self.password, "pointsEasy": self._pointsEasy, "pointsMedium": self._pointsMedium, "pointsHard": self._pointsHard}

    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            # add prepares to persist person object to Users table
            db.session.add(self)
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "username": self.name,
            "password": self.uid,
            "pointsEasy": self.pointsEasy,
            "pointsMedium": self.pointsMedium,
            "pointsHard": self.pointsHard
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, username="", password="", pointsEasy="", pointsMedium="", pointsHard=""):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if len(pointsEasy) > 0:
            self.pointsEasy = pointsEasy
        if len(pointsMedium) > 0:
            self.pointsMedium = pointsMedium
        if len(pointsHard) > 0:
            self.pointsHard = pointsHard
        if len(password) > 0:
            self.set_password(password)
        db.session.add(self)  # performs update when id exists
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


def init_leaderboards():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    l1 = Leaderboard(username="bob", password="apple",
                     pointsEasy=2, pointsMedium=5, pointsHard=3)
    l2 = Leaderboard(username="bobby", password="appley",
                     pointsEasy=20, pointsMedium=50, pointsHard=30)
    l3 = Leaderboard(username="bobbert", password="appled",
                     pointsEasy=200, pointsMedium=500, pointsHard=300)

    leaderboards = [l1, l2, l3]

    """Builds sample user/note(s) data"""
    for l in leaderboards:
        try:
            '''add user to table'''
            object = l.create()
            print(f"Created new uid {object.username}")
            db.session.add(l)
            db.session.commit()
        except:  # error raised if object nit created
            '''fails with bad or duplicate data'''
            print(f"Records exist uid {l.username}, or error.")
