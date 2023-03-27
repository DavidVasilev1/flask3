from sqlalchemy import Column, Integer, String, Text
from .. import db
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