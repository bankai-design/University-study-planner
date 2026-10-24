from app import db

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password