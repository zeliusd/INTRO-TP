from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Games(db.Model):
    __tablename__ = "games_tb"
    appid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    about_the_game = db.Column(db.Text, nullable=False)
    developers = db.Column(db.String(255), nullable=False)
    header_image = db.Column(db.String(255), nullable=False)
    categories = db.Column(db.String(255), nullable=False)

class Users(db.Model):
    __tablename__ = "users_tb"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    cant_reviews = db.Column(db.Integer, nullable=True)

class Reviews(db.Model):
    __tablename__ = "review_tb"
    review_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    appid = db.Column(db.ForeignKey('games_tb.appid') ,nullable=False)
    user_id = db.Column(db.ForeignKey('users_tb.user_id') ,nullable=False)
