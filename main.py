from flask_cors import CORS
from flask import render_template, url_for
from nighthawkguessr_api import app, db, project_path
from pathlib import Path
from nighthawkguessr_api.api.todo import todo_bp
from flask import send_from_directory
from nighthawkguessr_api.model.images import initEasyImages

from nighthawkguessr_api.model.leaderboards import init_leaderboards

from nighthawkguessr_api.api.leaderboard import leaderboard_bp


app.register_blueprint(todo_bp)
app.register_blueprint(leaderboard_bp)


@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        initEasyImages()
        init_leaderboards()


@app.route('/')
def index():
    return render_template('index.html')

# app.add_url_rule('/photos/<path:filename>', endpoint='photos', view_func=app.send_static_file)
# @app.route('/')
# def photo():
#     image_dir = Path.cwd()/"images/easy"
#     images_paths = [i.posix() for i in image_dir.iterdir()]
#     images = [Images("/image/easy/" + image, 250, 250, 1) for image in images_paths]
#     return render_template('photo1.html')

# @app.route('/')
# def capture_image(self):
#     self.cam = cv2.VideoCapture(0)
#     self.img = self.cam.read()
#     self.cam.release()
#     render_template(index.html,ob=self.img)


@app.route('/static/images/easy/<path:path>')
def send_report(path):
    full_filename = project_path.as_posix() + path
    # url_for('static', filename=f'images/easy/{path}')
    return render_template("image_template.html", user_image=path)


if __name__ == "__main__":
    cors = CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8200")
