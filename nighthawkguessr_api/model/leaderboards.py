from sqlalchemy import Column, Integer, String, Text
from nighthawkguessr_api import db
from sqlalchemy.exc import IntegrityError
import json

# 
# Leaderboard DB class that maps leaderboard SQL table 
#
class Leaderboard(db.Model):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True)
    _username = Column(String(255), unique=True, nullable=False)
    _pointsEasy = Column(Integer, nullable=False)
    _pointsMedium = Column(Integer, nullable=False)
    _pointsHard = Column(Integer, nullable=False)

    # 
    # Leaderboard DB class constructor 
    #
    def __init__(self, username, pointsEasy, pointsMedium, pointsHard):
        self._username = username
        self._pointsEasy = pointsEasy
        self._pointsMedium = pointsMedium
        self._pointsHard = pointsHard

    # 
    # Leaderboard DB class string representation of an object
    #
    def __repr__(self):
        return "<Leaderboard(id='%s', username='%s', pointsEasy='%s', pointsMedium='%s', pointsHard='%s')>" % (
            self.id,
            self.username,
            self.pointsEasy,
            self.pointsMedium,
            self.pointsHard,
        )

    # 
    # Returns Leaderboard username
    #    
    @property
    def username(self):
        return self._username

    # 
    # Sets Leaderboard username
    #        
    @username.setter
    def username(self, value):
        self._username = value

    # 
    # checks Leaderboard username valid
    #            
    def is_username(self, username):
        return self._username == username

    # 
    # Returns Leaderboard easy points
    #        
    @property
    def pointsEasy(self):
        return self._pointsEasy

    # 
    # Sets Leaderboard easy points
    #        
    @pointsEasy.setter
    def pointsEasy(self, value):
        self._pointsEasy = value

    # 
    # Sets Leaderboard medium points
    #            
    @property
    def pointsMedium(self):
        return self._pointsMedium

    # 
    # Sets Leaderboard medium points
    #        
    @pointsMedium.setter
    def pointsMedium(self, value):
        self._pointsMedium = value

    # 
    # Returns Leaderboard hard points
    #            
    @property
    def pointsHard(self):
        return self._pointsHard

    # 
    # Sets Leaderboard hard points
    #        
    @pointsHard.setter
    def pointsHard(self, value):
        self._pointsHard = value


    # 
    # Converts Leaderboard to dictionary
    #            
    def to_dict(self):
        return {"id": self.id, "username": self.username, "pointsEasy": self._pointsEasy, "pointsMedium": self._pointsMedium, "pointsHard": self._pointsHard}

    # 
    # Converts Leaderboard to string values
    #                
    def __str__(self):
        return json.dumps(self.read())

    # 
    # Creates Leaderboard database
    #                
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None
    # 
    # Returns Leaderboard name value pairs
    #            
    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "pointsEasy": self.pointsEasy,
            "pointsMedium": self.pointsMedium,
            "pointsHard": self.pointsHard
        }

    # 
    # Updates Leaderboard DB rows for points and user data
    #                
    def update(self, username="", pointsEasy="", pointsMedium="", pointsHard=""):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if len(pointsEasy) > 0:
            self.pointsEasy = pointsEasy
        if len(pointsMedium) > 0:
            self.pointsMedium = pointsMedium
        if len(pointsHard) > 0:
            self.pointsHard = pointsHard
        db.session.add(self)
        db.session.commit()
        return self

    # 
    # Delets Leaderboard row from teh DB
    #                
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # 
    # Initializes Leaderboard DB with test data
    #            
def init_leaderboards():
    """Create database and tables"""
    # db.create_all()
    """Tester data for table"""
    l1 = Leaderboard(username="bob",
                     pointsEasy=100, pointsMedium=700, pointsHard=1200)
    l2 = Leaderboard(username="bobby",
                     pointsEasy=200, pointsMedium=800, pointsHard=1100)
    l3 = Leaderboard(username="bobbert",
                     pointsEasy=300, pointsMedium=900, pointsHard=1000)
    l4 = Leaderboard(username="bobruth",
                     pointsEasy=400, pointsMedium=1000, pointsHard=900)
    l5 = Leaderboard(username="joe",
                     pointsEasy=500, pointsMedium=1100, pointsHard=800)
    l6 = Leaderboard(username="jo",
                     pointsEasy=600, pointsMedium=1200, pointsHard=700)
    l7 = Leaderboard(username="john",
                     pointsEasy=700, pointsMedium=100, pointsHard=600)
    l8 = Leaderboard(username="jon",
                     pointsEasy=800, pointsMedium=200, pointsHard=500)
    l9 = Leaderboard(username="jonny",
                     pointsEasy=900, pointsMedium=300, pointsHard=400)
    l10 = Leaderboard(username="johny",
                     pointsEasy=1000, pointsMedium=400, pointsHard=300)
    l11 = Leaderboard(username="johnathan",
                     pointsEasy=1100, pointsMedium=500, pointsHard=200)
    l12 = Leaderboard(username="jean",
                     pointsEasy=1200, pointsMedium=600, pointsHard=100)
    leaderboards = [l1, l2, l3, l4,l5,l6,l7,l8,l9,l10,l11,l12]

    """Builds sample user/note(s) data"""
    for l in leaderboards:
        try:
            '''add user to table'''
            object = l.create()
            print(f"Created new uid {object.username}")
            db.session.add(l)
            db.session.commit()
        except:
            '''fails with bad or duplicate data'''
            print(f"Records exist uid {l.username}, or error.")
