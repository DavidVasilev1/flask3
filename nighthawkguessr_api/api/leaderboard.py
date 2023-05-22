from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from nighthawkguessr_api import db
from nighthawkguessr_api.model.leaderboards import Leaderboard

leaderboard_bp = Blueprint("leaderboards", __name__, url_prefix="/api/leaderboard")
leaderboard_api = Api(leaderboard_bp)

def get_user_list():
    users_list = [[user._username, int(user._pointsEasy)+2*int(user._pointsMedium)+3*int(user._pointsHard), user._pointsEasy, user._pointsMedium, user._pointsHard] for user in Leaderboard.query.all()]
    return users_list

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
                user.pointsEasy = int(request.get_json().get("pointsEasy"))
                user.pointsMedium = int(request.get_json().get("pointsMedium"))
                user.pointsHard = int(request.get_json().get("pointsHard"))
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
        
class LeaderboardTop10(Resource):
    def partition(self, arr, lo, hi):
        pivot = arr[hi][1]
        i = lo - 1
        for j in range(lo, hi):
            if arr[j][1] >= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i+1
    
    def qSortUserList(self, arr, lo, hi):
        if lo < hi:
            part = self.partition(arr, lo, hi)
            self.qSortUserList(arr, lo, part-1)
            self.qSortUserList(arr, part+1, hi)

    def get(self):
        users_list = get_user_list()
        top10 = []
        self.qSortUserList(users_list, 0, len(users_list)-1)
        print(users_list)
        for user in users_list:
            top10.append({"username": user[0], "total": user[1], "Easy":user[2], "Medium":user[3], "Hard":user[4]})
        print(top10)
        if len(top10) <= 10:
            return top10
        return top10
        # return top10[:10]

# Leaderboard Security provides Authentication mechanism    
class LeaderboardSecurity(Resource):

    def post(self):
        ''' Read data for json body '''
        body = request.get_json()
        
        ''' Get Data '''
        username = body.get('username')
        if username is None or len(username) < 1:
            return {'message': f'User ID is missing, or is less than 2 characters'}, 400
        password = body.get('password')
        # print("LeaderboardSecurity: post(): username: " + username + " password: " + password)
        # print("LeaderboardSecurity: post(): password-hash: " + generate_password_hash(password))
        
        ''' Find user '''
        user = Leaderboard.query.filter_by(_username=username).first()          
        if user is None or not user.is_password(password):
            return {'message': f"Invalid user id or password"}, 400
        
        ''' authenticated user '''
        return jsonify(user.read())

# Leaderboard APIs

leaderboard_api.add_resource(LeaderboardAPI, "/leaderboard")
leaderboard_api.add_resource(LeaderboardListAPI, "/leaderboardList")
leaderboard_api.add_resource(LeaderboardTop10, "/leaderboardTop10")
leaderboard_api.add_resource(LeaderboardSecurity, "/authenticate")
