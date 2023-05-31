from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from nighthawkguessr_api import db
from nighthawkguessr_api.model.leaderboards import Leaderboard
import base64

leaderboard_bp = Blueprint("leaderboards", __name__, url_prefix="/api/leaderboard")
leaderboard_api = Api(leaderboard_bp)

def get_total_user_list():
    total_users_list = [[user._username, int(user._pointsEasy)+2*int(user._pointsMedium)+3*int(user._pointsHard), int(user._pointsEasy), 2*int(user._pointsMedium), 3*int(user._pointsHard)] for user in Leaderboard.query.all()]
    return total_users_list

def get_easy_user_list():
    easy_users_list = [[user._username, int(user._pointsEasy)+2*int(user._pointsMedium)+3*int(user._pointsHard), int(user._pointsEasy), 2*int(user._pointsMedium), 3*int(user._pointsHard)] for user in Leaderboard.query.all()]
    return easy_users_list

def get_medium_user_list():
    medium_users_list = [[user._username, int(user._pointsEasy)+2*int(user._pointsMedium)+3*int(user._pointsHard), int(user._pointsEasy), 2*int(user._pointsMedium), 3*int(user._pointsHard)] for user in Leaderboard.query.all()]
    return medium_users_list

def get_hard_user_list():
    hard_users_list = [[user._username, int(user._pointsEasy)+2*int(user._pointsMedium)+3*int(user._pointsHard), int(user._pointsEasy), 2*int(user._pointsMedium), 3*int(user._pointsHard)] for user in Leaderboard.query.all()]
    return hard_users_list

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
    def partition(self, arr, lo, hi,level):
        pivot = arr[hi][level]
        i = lo - 1
        for j in range(lo, hi):
            if arr[j][level] >= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i+1
    
    def qSortUserList(self, arr, lo, hi,level):
        if lo < hi:
            part = self.partition(arr, lo, hi,level)
            self.qSortUserList(arr, lo, part-1,level)
            self.qSortUserList(arr, part+1, hi,level)

    def get(self):
        top10all = {}
        total_users_list = get_total_user_list()
        top10total = []
        self.qSortUserList(total_users_list, 0, len(total_users_list)-1,1)
        print(total_users_list)
        for user in total_users_list:
            top10total.append({"username": user[0], "total": user[1], "Easy":user[2], "Medium":user[3], "Hard":user[4]})
        print(top10total)
        if len(top10total) <= 10:
            # return top10total
            top10all["TotalSort"]=(top10total)
        else:
            # return top10total[:10]
            top10all["TotalSort"]=(top10total[:10])
    
        easy_users_list = get_easy_user_list()
        top10easy = []
        self.qSortUserList(easy_users_list, 0, len(easy_users_list)-1,2)
        print(easy_users_list)
        for user in easy_users_list:
            top10easy.append({"username": user[0], "total": user[1], "Easy":user[2], "Medium":user[3], "Hard":user[4]})
        print(top10easy)
        if len(top10easy) <= 10:
            top10all["EasySort"]=(top10easy)
        else:
            top10all["EasySort"]=(top10easy[:10])
    
        medium_users_list = get_medium_user_list()
        top10medium = []
        self.qSortUserList(medium_users_list, 0, len(medium_users_list)-1,3)
        print(medium_users_list)
        for user in medium_users_list:
            top10medium.append({"username": user[0], "total": user[1], "Easy":user[2], "Medium":user[3], "Hard":user[4]})
        print(top10medium)
        if len(top10medium) <= 10:
            top10all["MediumSort"]=(top10medium)
        else:
            top10all["MediumSort"]=(top10medium[:10])
    
        hard_users_list = get_hard_user_list()
        top10hard = []
        self.qSortUserList(hard_users_list, 0, len(hard_users_list)-1,4)
        print(hard_users_list)
        for user in hard_users_list:
            top10hard.append({"username": user[0], "total": user[1], "Easy":user[2], "Medium":user[3], "Hard":user[4]})
        print(top10hard)
        if len(top10hard) <= 10:
            top10all["HardSort"]=(top10hard)
        else:
            top10all["HardSort"]=(top10hard[:10])
        
        return top10all
# Leaderboard Security provides Authentication mechanism    
# class LeaderboardSecurity(Resource):

#     def post(self):
#         ''' Read data for json body '''
#         body = request.get_json()
        
#         ''' Get Data '''
#         username = body.get('username')
#         if username is None or len(username) < 1:
#             return {'message': f'User ID is missing, or is less than 2 characters'}, 400
#         password = body.get('password')
#         # print("LeaderboardSecurity: post(): username: " + username + " password: " + password)
#         # print("LeaderboardSecurity: post(): password-hash: " + generate_password_hash(password))
        
#         ''' Find user '''
#         user = Leaderboard.query.filter_by(_username=username).first()          
#         if user is None or not user.is_password(password):
#             return {'message': f"Invalid user id or password"}, 400
        
#         ''' authenticated user '''
#         return jsonify(user.read())


class _Authenticate(Resource):
    def post(self):
        body = request.get_json()
        username = body.get('username')
        password = body.get('password')
        if len(username) < 1:
            return {'message': f'Invalid username'}, 210
        if len(password) < 1:
            return {'message': f'Empty Password'}, 210
        user = find_by_username(username)
        print(user)
        if user.is_password(password):
            password = user.getFullPassword()
            pwbytes=password.encode("ascii")
            b64pw_bytes=base64.b64encode(pwbytes)
            unique=str(b64pw_bytes)[15:25]
            return username + ":" + unique
        return None
    
class _wap(Resource):
    def post(self):
        body = request.get_json()
        username = body.get('username')
        key = body.get('key')
        if len(username) < 1:
            return {'message': f'Invalid username'}, 210
        if len(key) < 1:
            return {'message': f'Empty key'}, 210
        user = find_by_username(username)
        password = user.getFullPassword()
        pwbytes=password.encode("ascii")
        b64pw_bytes=base64.b64encode(pwbytes)
        unique=str(b64pw_bytes)[15:25]
        print(unique)
        if key == unique:
            return True
        return False

# Leaderboard APIs

leaderboard_api.add_resource(LeaderboardAPI, "/leaderboard")
leaderboard_api.add_resource(LeaderboardListAPI, "/leaderboardList")
leaderboard_api.add_resource(LeaderboardTop10, "/leaderboardTop10")
# leaderboard_api.add_resource(LeaderboardSecurity, "/authenticate")
leaderboard_api.add_resource(_Authenticate, "/auth")
leaderboard_api.add_resource(_wap, "/wap")
