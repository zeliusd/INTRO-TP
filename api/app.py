from flask import Flask, jsonify, request
from sqlalchemy.util import NoneType
from tables.tables import db, Reviews, Users, Games
from flask_cors import CORS
from sqlalchemy import event

app = Flask(__name__)

CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:postgres@db:5432/games_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.reflect()
    db.Model.metadata.create_all(db.engine)
    db.create_all()


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


@app.route("/users/<int:user_id>", methods=["GET"])
def user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "No hay usuario disponible"})

    user_data = {
        "id": user.user_id,
        "username": user.username,
        "cant_reviews": user.cant_reviews,
    }
    return jsonify(user_data)


@app.route("/users", methods=["GET"])
def users():
    username = request.args.get("username")
    users_data = []
    query = Users.query.filter_by(username=username).first()
    if not query:
        query = Users.query.all()
        if not query:
            return jsonify({"message": "No hay usuarios disponibles"})

        for user in query:
            user_data = {
                "id": user.user_id,
                "username": user.username,
                "cant_reviews": user.cant_reviews,
            }
            users_data.append(user_data)
    else:
        users_data = [
            {
                "id": query.user_id,
                "username": query.username,
                "cant_reviews": query.cant_reviews,
            }
        ]
    return jsonify(users_data)


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = Users.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        if "username" in data:
            user.username = data["username"]
        if "cant_reviews" in data:
            user.cant_reviews = data["cant_reviews"]
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Invalid data: {e}"}), 400


def add_user(username):
    try:
        new_user = Users(username=username)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User added successfully"}, new_user.user_id
    except Exception as e:
        print(e)
        return None, e


@app.route("/users", methods=["POST"])
def new_user():
    data = request.get_json()
    username = data["username"]
    if not username:
        return jsonify({"message": "Bad Request"}), 400

    user, _ = add_user(username)
    if not user:
        return jsonify({"message": "Internal error"}), 500

    return jsonify(user), 200


def load_reviews(query):
    if not query:
        return None
    reviews_data = [
        {
            "review_id": reviews.review_id,
            "comment": reviews.comment,
            "score": reviews.score,
            "date": reviews.date,
            "appid": reviews.appid,
            "username": username,
            "user_id": reviews.user_id,
        }
        for reviews, username in query
    ]
    return reviews_data


@app.route("/reviews", methods=["POST"])
def add_review():
    data = request.get_json()
    comment = data["comment"]
    score = data["score"]
    appid = data["appid"]
    username = data["username"]
    if not comment or not score or not appid or not username:
        return jsonify({"message:": "Bad request"})

    user = Users.query.filter_by(username=username).first()

    if not user:
        _, id = add_user(username)
        user_id = id
    else:
        user_id = user.user_id

    if not user_id:
        return jsonify({"message:": "Internal error"})
    try:
        new_review = Reviews(comment=comment, score=score, appid=appid, user_id=user_id)
        db.session.add(new_review)
        db.session.flush()
        user = Users.query.get(new_review.user_id)
        if user:
            user.cant_reviews = (user.cant_reviews or 0) + 1

        db.session.commit()
        return jsonify({"message:": "Review added successfully"}), 201
    except Exception as e:
        return jsonify({"message:" f"Internal error {e}"})


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = Users.query.get(user_id)
        if user is None:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify(
            {"message": "User and associated reviews deleted successfully"}
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@app.route("/reviews/<int:review_id>", methods=["PUT"])
def edit_review(review_id):
    data = request.get_json()
    comment = data["comment"]
    score = data["score"]
    if not comment or not score:
        return jsonify({"message": "Bad request"}), 400
    try:
        review = Reviews.query.get(review_id)
        if review is None:
            return jsonify({"message": "Review not found"}), 404
        review.comment = comment
        review.score = score
        db.session.commit()
        return jsonify({"message": "Review updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@app.route("/reviews/<int:review_id>", methods=["GET"])
def review(review_id):
    review = Reviews.query.get(review_id)
    if not review:
        return jsonify({"message": "Review not found"}), 404
    review_data = {
        "review_id": review.review_id,
        "comment": review.comment,
        "score": review.score,
        "date": review.date,
        "appid": review.appid,
        "user_id": review.user_id,
    }
    return jsonify(review_data)


@app.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    try:
        review = Reviews.query.get(review_id)
        if review is None:
            return jsonify({"message": "Review not found"}), 404

        db.session.delete(review)
        user = Users.query.get(review.user_id)
        if user:
            user.cant_reviews = (user.cant_reviews or 0) - 1

        db.session.commit()
        return jsonify({"message": "Review deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@app.route("/users/<int:user_id>/reviews", methods=["GET"])
def user_reviews(user_id):
    reviews = load_reviews(Reviews.query.filter_by(user_id=user_id).all())
    if not reviews:
        return jsonify({"message:": "Bad request"})
    return jsonify(reviews)


@app.route("/games/<int:appid>/reviews", methods=["GET"])
def game_reviews(appid):
    reviews = load_reviews(
        db.session.query(Reviews, Users.username)
        .filter_by(appid=appid)
        .join(Users, Reviews.user_id == Users.user_id)
        .all()
    )
    if not reviews:
        return jsonify({"message:": "Bad request"})
    return jsonify(reviews)


app.run(debug=True)
