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
