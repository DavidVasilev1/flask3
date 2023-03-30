from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.images import Images
 
images_bp = Blueprint("images", __name__)
images_api = Api(images_bp)

class ImagesAPI(Resource):
    def get(self):
        id = request.args.get("id")
        image = db.session.query(Images).get(id)
        if image:
            path = image.imagePath
        