#!/usr/bin/env python3
from nighthawkguessr_api import app, db, model
print(app.config["SQLALCHEMY_DATABASE_URI"])
with app.app_context():
    db.create_all()
    db.session.commit

