from sqlalchemy import Column, Integer, String, Text, LargeBinary
from .. import db
from pathlib import Path


class Images(db.Model):
    __tablename__ = "images"
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


def initEasyImages():
    image_dir = Path.cwd().parents[1]/"images/easy"
    images_paths = [i.as_posix() for i in image_dir.iterdir()]
    images = []
    for image in images_paths:
        images.append(Images(image, 250, 250, 1))
    print()
# def initMedImages():
# def initHardImages():

# def initImages():

initEasyImages()