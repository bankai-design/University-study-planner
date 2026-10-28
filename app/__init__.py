from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def createApp():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
    app.secret_key = "this-is-my-secret-key"
    db.init_app(app)

    from app.auth.auth import authBP
    from app.dash.dash import dashBP

    app.register_blueprint(authBP, url_prefix="/auth")
    app.register_blueprint(dashBP, url_prefix="/dash")

    with app.app_context():
        db.create_all()

    return app