from flask_cors import CORS
from flask import render_template
from nighthawkguessr_api import app, db

from nighthawkguessr_api.api.todo import todo_bp

from nighthawkguessr_api.model.images import initEasyImages

from nighthawkguessr_api.api.leaderboard import leaderboard_bp


app.register_blueprint(todo_bp)
app.register_blueprint(leaderboard_bp)

@app.before_first_request
def init_db():
    with app.app_context():
        initEasyImages()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    cors = CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8200")
