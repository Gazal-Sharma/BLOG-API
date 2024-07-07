from db_run import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class Comments(db.Model):
    __tablename__ = 'Comments'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10), db.ForeignKey('blogpost.Post_Title'), nullable=False)
    username_comm = db.Column(db.String(80), db.ForeignKey('users.u_username'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    blog_title = db.relationship('BlogPost', foreign_keys = ['title'],  backref=db.backref('comments', lazy=True))
    user_com = db.relationship('User', foreign_keys = ['username_comm'], backref=db.backref('comments', lazy=True))
    