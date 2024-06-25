from flask import Flask, jsonify, request
from tables.games import Games, db
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:postgres@db:5432/games_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def games_data(query_results):

    if not query_results:
        return None

    games_data = [
        {
            "id": game.appid,
            "name": game.name,
            "price": game.price,
            "about": game.about_the_game,
            "developer": game.developers,
            "image": game.header_image,
            "categories": game.categories.split(",") if game.categories else [],
        }
        for game in query_results
    ]
    return games_data


def game_data(query_results):
    if not query_results:
        return None

    game_data = {
        "id": query_results.appid,
        "name": query_results.name,
        "price": query_results.price,
        "about": query_results.about_the_game,
        "developer": query_results.developers,
        "image": query_results.header_image,
        "categories": (
            query_results.categories.split(",") if query_results.categories else []
        ),
    }
    return game_data


@app.route("/")
def hello():
    return "<h1>¡Docker funciona correctamente!</h1>"


@app.route("/games", methods=["GET"])
def games():
    limits = request.args.get("limit")
    data = None
    if limits:
        data = games_data(Games.query.order_by(Games.appid).limit(int(limits)).all())
    else:
        data = games_data(Games.query.all())

    if not data:
        return jsonify({"message": "No hay juegos disponibles"}), 404
    return jsonify(data)


@app.route("/games/<int:appid>", methods=["GET"])
def game(appid):
    data = game_data(Games.query.get(appid))
    if not data:
        return jsonify({"message": "Juego no encontrado"}), 404
    return jsonify(data)


@app.route("/games/filter", methods=["GET"])
def filter_games():
    name = request.args.get("name")
    developer = request.args.get("developer")
    category = request.args.get("category")
    if not name and not developer and not category:
        return jsonify({"message": "No hay filtros disponibles"}), 400
    query = Games.query
    if name:
        query = query.filter(Games.name.ilike(f"%{name}%"))
    if developer:
        query = query.filter(Games.developers.ilike(f"%{developer}%"))
    if category:
        query = query.filter(Games.categories.ilike(f"%{category}%"))
    data = games_data(query.all())
    if not data:
        return jsonify({"message": "No hay juegos disponibles"}), 404
    return jsonify(data)


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
