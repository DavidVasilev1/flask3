from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.leaderboards import Leaderboard

leaderboard_bp = Blueprint("leaderboards", __name__)
leaderboard_api = Api(leaderboard_bp)

def get_user_list():
    users_list = [[user._username, int(user._pointsEasy)+2*int(user._pointsMedium)+3*int(user._pointsHard)] for user in Leaderboard.query.all()]
    return users_list

class LeaderboardAPI(Resource):
    def get(self):
        username = request.args.get("id")
        print(username, "uid")
        leaderboard = db.session.query(Leaderboard).get(username)
        print(leaderboard, "?")
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
        
class LeaderboardTop10(Resource):
    def partition(self, arr, lo, hi):
        pivot = arr[hi][1]
        i = lo - 1
        for j in range(lo, hi):
            if arr[j][1] >= pivot:
                i = i + 1
                (arr[i], arr[j]) = (arr[j], arr[i])
        (arr[i + 1], arr[hi]) = (arr[hi], arr[i + 1])
        return i+1
    
    def qSortUserList(self, arr, lo, hi):
        if lo < hi:
            part = self.partition(arr, lo, hi)
            self.qSortUserList(arr, lo, part-1)
            self.qSortUserList(arr, part+1, hi)

    def get(self):
        users_list = get_user_list()
        top10 = {}
        self.qSortUserList(users_list, 0, len(users_list)-1)
        for user in users_list:
            top10[user[0]] = user[1]
        print(top10)
        if len(top10) <= 10:
            return top10
        return top10[:10]
        



leaderboard_api.add_resource(LeaderboardAPI, "/leaderboard")
leaderboard_api.add_resource(LeaderboardListAPI, "/leaderboardList")
leaderboard_api.add_resource(LeaderboardTop10, "/leaderboardTop10")
