from flask import Flask

def createApp():
    app = Flask(__name__)

    from app.auth.auth import authBP

    app.register_blueprint(authBP, url_prefix="/auth")

    return app