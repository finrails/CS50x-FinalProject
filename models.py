from app import db
from sqlalchemy import ForeignKey

class User(db.Model): # pyright: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id))
    body = db.Column(db.String(255), nullable=False)
    checked = db.Column(db.String(3))
    created_at = db.Column(db.Text, nullable=False)
