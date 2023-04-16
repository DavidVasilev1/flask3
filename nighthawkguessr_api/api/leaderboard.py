from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.leaderboards import Leaderboard

leaderboard_bp = Blueprint("leaderboards", __name__)
leaderboard_api = Api(leaderboard_bp)


def find_by_username(username):
    users = Leaderboard.query.filter_by(_username=username).all()
    return users[0]


class LeaderboardAPI(Resource):
    def get(self):
        username = request.get_json().get("username")
        print(username, "uid")
        user = find_by_username(username)
        if user:
            return user.to_dict()
        return {"message": user}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        parser.add_argument("password", required=True, type=str)
        parser.add_argument("pointsEasy", required=True, type=int)
        parser.add_argument("pointsMedium", required=True, type=int)
        parser.add_argument("pointsHard", required=True, type=int)
        args = parser.parse_args()

        leaderboard = Leaderboard(args["username"], args["password"],
                                  args["pointsEasy"], args["pointsMedium"], args["pointsHard"])
        try:
            db.session.add(leaderboard)
            db.session.commit()
            return leaderboard.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def put(self):
        username = request.get_json().get("username")
        print(username, "uid")

        try:
            user = find_by_username(username)
            if user:
                user.pointsEasy = int(request.get_json().get(
                    "pointsEasy"))
                user.pointsMedium = int(request.get_json().get(
                    "pointsMedium"))
                user.pointsHard = int(request.get_json().get(
                    "pointsHard"))
                db.session.commit()
                return user.to_dict(), 201
            else:
                return {"message": "leaderboard not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        username = request.get_json().get("username")
        print(username, "uid")

        try:
            user = find_by_username(username)
            if user:
                db.session.delete(user)
                db.session.commit()
                return user.to_dict()
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
