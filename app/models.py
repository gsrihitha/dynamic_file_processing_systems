from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.pwd_hash, password)

