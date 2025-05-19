from flask_login import UserMixin
from iris.extensions import db
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    ms_id = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    display_name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    job_title = db.Column(db.String(255))
    department = db.Column(db.String(255))
    profile_picture = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.display_name}>'
    