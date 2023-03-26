from flask_cors import CORS
from flask import render_template
from kaedenn_api import app, db

from kaedenn_api.api.todo import todo_bp

from kaedenn_api.model.todos import init_todos

app.register_blueprint(todo_bp)

@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        init_todos()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    cors = CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8200")
