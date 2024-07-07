from db_run import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


class Blogpost(db.Model):
    __tablename__ = 'BlogPost'

    id = db.Column(db.Integer, primary_key=True)
    username_post = db.Column(db.String(80), db.ForeignKey('users.u_username'), nullable=False)
    title = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', foreign_keys = [username_post], backref=db.backref('posts', lazy=True))