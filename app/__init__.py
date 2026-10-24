from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def createApp():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
    app.secret_key = "this-is-my-secret-key"
    db.init_app(app)

    from app.auth.auth import authBP

    app.register_blueprint(authBP, url_prefix="/auth")

    with app.app_context():
        db.create_all()

    return app