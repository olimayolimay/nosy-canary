from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Notice I am NOT importing app.py here.
# I rely on db being passed in from app.py before creating tables.
# The simplest solution is to define db = SQLAlchemy() here and then initialize it in app.py.

# Define a global SQLAlchemy instance that will be initialized later:
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(64), unique=True, nullable=False)
    canary_bedtime = db.Column(db.String(5), nullable=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(32), default='pending')
    notes = db.Column(db.Text, nullable=True)
    user = db.relationship('User', backref='tasks', lazy=True)

class Intention(db.Model):
    __tablename__ = 'intentions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='intentions', lazy=True)

