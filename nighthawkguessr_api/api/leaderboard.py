from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.leaderboards import Leaderboard

leaderboard_bp = Blueprint("leaderboards", __name__)
leaderboard_api = Api(leaderboard_bp)


class LeaderboardAPI(Resource):
    def get(self):
        username = request.args.get("username")
        leaderboard = db.session.query(Leaderboard).get(username)
        if leaderboard:
            return leaderboard.to_dict()
        return {"message": leaderboard}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        parser.add_argument("password", required=True, type=str)
        parser.add_argument("pointsEasy", required=True, type=int)
        parser.add_argument("pointsMedium", required=True, type=int)
        parser.add_argument("pointsHard", required=True, type=int)
        args = parser.parse_args()

        leaderboard = Leaderboard(args["username"], args["password"], args["pointsEasy"], args["pointsMedium"], args["pointsHard"])
        try:
            db.session.add(leaderboard)
            db.session.commit()
            return leaderboard.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        args = parser.parse_args()

        try:
            leaderboard = db.session.query(Leaderboard).get(args["username"])
            if leaderboard:
                leaderboard.pointsEasy = args["pointsEasy"]
                leaderboard.pointsMedium = args["pointsMedium"]
                leaderboard.pointsHard = args["pointsHard"]
                db.session.commit()
            else:
                return {"message": "leaderboard not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        args = parser.parse_args()

        try:
            leaderboard = db.session.query(Leaderboard).get(args["username"])
            if leaderboard:
                db.session.delete(leaderboard)
                db.session.commit()
                return leaderboard.to_dict()
            else:
                return {"message": "leaderboard not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500


class LeaderboardListAPI(Resource):
    def get(self):
        try:
            leaderboards = db.session.query(Leaderboard).all()
            return [leaderboard.to_dict() for leaderboard in leaderboards]
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        try:
            db.session.query(Leaderboard).delete()
            db.session.commit()
            return []
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500


leaderboard_api.add_resource(LeaderboardAPI, "/leaderboard")
leaderboard_api.add_resource(LeaderboardListAPI, "/leaderboardList")
