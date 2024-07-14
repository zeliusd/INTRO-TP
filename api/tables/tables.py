import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Games(db.Model):
    __tablename__ = "games_tb"
    appid = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    about_the_game = db.Column(db.Text, nullable=False)
    developers = db.Column(db.String(255), nullable=False)
    header_image = db.Column(db.String(255), nullable=False)
    categories = db.Column(db.String(255), nullable=False)
    reviews = db.relationship("Reviews")


class Users(db.Model):
    __tablename__ = "users_tb"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    cant_reviews = db.Column(db.Integer, nullable=True, default=0)
    reviews = db.relationship("Reviews", backref="user", lazy=True)


class Reviews(db.Model):
    __tablename__ = "review_tb"
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(1000), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=datetime.datetime.now())
    appid = db.Column(db.Integer, db.ForeignKey("games_tb.appid"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users_tb.user_id"), nullable=False)
