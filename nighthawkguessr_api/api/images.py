from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from math import sqrt, exp, floor
from nighthawkguessr_api import project_path
from nighthawkguessr_api import db
from nighthawkguessr_api.model.todos import Todo
import os, random
import base64


 
images_bp = Blueprint("images", __name__, url_prefix='/api/images')
images_api = Api(images_bp)

def get_random_easy_image():
    images = Images.query.filter_by(_difficulty=0).all()
    image = random.choice(images)
    return image

def get_random_medium_image():
    images = Images.query.filter_by(_difficulty=1).all
    image = random.choice(images)
    return image

def get_random_hard_image():
    images = Images.query.filter_by(_difficulty=2).all
    image = random.choice(images)
    return image

class ImagesAPI:
    class _EasyImages(Resource):
        def get(self):
            image = get_random_easy_image()
            json_data = {}
            if image:
                image_path = project_path + "/" + image.imagePath
                with open(image_path, "rb") as image_file:
                    json_data["bytes"] = str(base64.b64encode(image_file.read()))[2:][:-1]
                json_data["xCoord"] = image.xCoord
                json_data["yCoord"] = image.yCoord
            return jsonify(json_data)

    class _MediumImages(Resource):
        def get(self):
            image = get_random_medium_image()
            json_data = {}
            if image:
                image_path = project_path + "/" + image.imagePath
                with open(image_path, "rb") as image_file:
                    json_data["bytes"] = str(base64.b64encode(image_file.read()))
                json_data["xCoord"] = image.xCoord
                json_data["yCoord"] = image.yCoord
            return jsonify(json_data)

    class _HardImages(Resource):
        def get(self):
            image = get_random_hard_image()
            json_data = {}
            if image:
                image_path = project_path + "/" + image.imagePath
                with open(image_path, "rb") as image_file:
                    json_data["bytes"] = str(base64.b64encode(image_file.read()))
                json_data["xCoord"] = image.xCoord
                json_data["yCoord"] = image.yCoord
            return jsonify(json_data)
        
    class _CalculatePoints(Resource):
        def get(self):
            userXCoord = int(request.get_json().get("userXCoord"))
            userYCoord = int(request.get_json().get("userYCoord"))
            XCoord = int(request.get_json().get("XCoord"))
            YCoord = int(request.get_json().get("YCoord"))
            distance = sqrt((XCoord-userXCoord)**2 + (YCoord-userYCoord)**2)
            points = int(floor(5314.0934613321*exp(distance)-314.093461332))
            if points >= 0:
                return points
            return 0

    images_api.add_resource(_EasyImages, '/GetEasyImage')
    images_api.add_resource(_CalculatePoints, '/CalculatePoints')