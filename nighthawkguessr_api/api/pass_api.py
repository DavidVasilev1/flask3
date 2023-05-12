import requests
import random
import string
from flask import Blueprint, jsonify

pass_api = Blueprint('pass_api', __name__, url_prefix='/api/pass')

def getPassAPI(length=3):
    password = []
    url = "https://random-words5.p.rapidapi.com/getMultipleRandom"
    querystring = {"count": str(length)}
    headers = {
        "X-RapidAPI-Key": "f0aeb431bamshc18b522b64e7383p102f67jsnea4673acfc55",
        "X-RapidAPI-Host": "random-words5.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    words = response.json()
    password += words
    num_random_chars = (length * 2) - len(words)
    password += [random.choice(string.ascii_letters + string.digits) for i in range(num_random_chars)]
    random.shuffle(password)
    response = ''.join(password)
    return response

@pass_api.route('/generate_password', methods=['GET'])
def generate_password_api():
    password = getPassAPI(5)
    return jsonify({"password": password})


