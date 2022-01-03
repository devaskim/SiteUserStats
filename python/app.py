import flask
from flask import Flask
from flask import request

from visitors_stats.Constants import Constants
from visitors_stats.VisitorsStats import VisitorsStats

app = Flask(__name__)
stats = VisitorsStats({"host": "localhost",
                       "user": "username",
                       "database": "database",
                       "password": "password"})


@app.route(Constants.API_ENDPOINT_NEW_USER, methods=["POST"])
def add_user():
    return 200


@app.route(Constants.API_ENDPOINT_USERS, methods=["POST"])
def get_users():
    page = request.args.get('page', -1)
    return flask.jsonify(stats.get_users(page))


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
