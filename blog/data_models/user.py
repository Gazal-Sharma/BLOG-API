from db_run import db
from flask_sqlalchemy import SQLAlchemy

class Users(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(20), unique = True, nullable = False)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column()
    # posts = db.relationship('BlogPost', backref='author', lazy=True)
    # comments = db.relationship('Comments', backref='author', lazy=True)
