from sqlalchemy import Column, Integer, String, Text, LargeBinary
from sqlalchemy.exc import IntegrityError
from nighthawkguessr_api import db
from pathlib import Path


class Images(db.Model):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    _imagePath = Column(Text, unique=True, nullable=False)
    _xCoord = Column(Integer, nullable=False)
    _yCoord = Column(Integer, nullable=False)
    _difficulty = Column(Integer, nullable=False)

    
    def __init__(self, imagePath, xCoord, yCoord, difficulty):
        self._imagePath = imagePath
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.difficulty = difficulty

    def __repr__(self):
        return "<image(id='%s', imagePath='%s', xCoord='%s', yCoord='%s', difficulty='%s')>" % (
            self.id,
            self.imagePath,
            self.xCoord,
            self.yCoord,
            self.difficulty
        )
    @property
    def imagePath(self):
        return self._imagePath

    @imagePath.setter
    def imagePath(self, value):
        self._imagePath = value

    @property
    def xCoord(self):
        return self._xCoord

    @xCoord.setter
    def xCoord(self, value):
        self._xCoord = value

    @property
    def yCoord(self):
        return self._yCoord

    @yCoord.setter
    def yCoord(self, value):
        self._yCoord = value

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = value

    def to_dict(self):
        return {"id": self.id, "imagePath": self._imagePath, "xCoord": self._xCoord, "yCoord": self._yCoord, "difficulty": self._difficulty}

    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionaries
    # returns dictionary
    def read(self):
        return {
            "path": self.imagePath,
            "xCoord": self.xCoord,
            "yCoord": self.yCoord,
            "difficulty": self.difficulty
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, path="", xCoord="", yCoord="", difficulty=""):
        """only updates values with length"""
        xCoord = int(xCoord)
        yCoord = int(yCoord)
        if path:
            self.imagePath = path
        if xCoord >= 0:
            self.xCoord = xCoord
        if yCoord >= 0:
            self.yCoord = yCoord
        if difficulty in range(3):
            self.difficulty = difficulty
        db.session.commit()
        return self


    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


def initEasyImages(): 
    image_dir = Path.cwd()/"images/easy"
    images_paths = [i.name for i in image_dir.iterdir()]
    images = []
    for image in images_paths:
        print(image)
        xCoord = int(input("Enter X-Coordinate"))
        yCoord = int(input("Enter Y-Coordinate"))
        images.append(Images("images/easy/" + image, xCoord, yCoord, 0))
    for image in images:
        try:
            image.create()
            print("Successfully added entry")
        except:
            db.session.remove()
            print("Error adding image: ", image.imagePath)
    