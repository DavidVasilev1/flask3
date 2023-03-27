from sqlalchemy import Column, Integer, String, Text
from .. import db


class Images(db.Model):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    _image = Column(Text, unique=True, nullable=False)
    _xCoord = Column(String(255), nullable=False)
    _yCoord = Column(Integer, nullable=False)
    _difficulty = Column(Integer, nullable=False)

    
    def __init__(self, image, xCoord, yCoord, difficulty):
        self._image = image
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.difficulty = difficulty