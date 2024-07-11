from flask import Flask, jsonify, request
from tables.tables import db, Reviews, Users, Games
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:postgres@db:5432/games_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


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


# End point para todos los usuarios
@app.route("/users/", methods=["GET"])
def users():
    users = Users.query.all()
    users_data = []
    for user in users:
        user_data = {
            "id": user.user_id,
            "username": user.username,
            "cant_reviews": user.username,
        }
        users_data.append(user_data)
    if not users:
        return jsonify({"message": "No hay usuarios disponibles"})

    return jsonify(users_data)


# End point para crear un nuevo usuario
@app.route("/users/", methods=["POST"])
def new_user():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Bad request"}), 400
        username = data.get("username")
        if not username:
            return jsonify({"message": "Bad request"}), 400
        new_user = Users(username=username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            {"user": {"user_id": new_user.user_id, "username": new_user.username}}
        )
    except Exception as e:
        return jsonify({"message": f"Error al crear el usuario {e}"})


# End point para un usuario
@app.route("/users/<int:user_id>", methods=["GET"])
def user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "No hay usuario disponible"})

    user_data = {
        "id": user.user_id,
        "username": user.username,
        "cant_reviews": user.username,
    }
    return jsonify(user_data)


db.init_app(app)
with app.app_context():
    db.reflect()
    db.Model.metadata.create_all(db.engine)
    db.create_all()
app.run(debug=True)
