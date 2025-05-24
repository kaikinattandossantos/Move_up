from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    trainings = db.relationship('Training', backref='user', lazy=True)
    


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    muscle_group = db.Column(db.String(100))
    specific_muscle = db.Column(db.String(100))
    training_time = db.Column(db.String(100))
    plan_text = db.Column(db.Text)  # Aqui salva o plano
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())



plan_text = db.Column(db.Text)