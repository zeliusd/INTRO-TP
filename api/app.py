from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_geek():
    return "<h1>¡Docker funciona correctamente!</h2> <br> <h3> Hola </h3>"


if __name__ == "__main__":
    app.run(debug=True)
