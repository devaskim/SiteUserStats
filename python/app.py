import flask
from flask import Flask
from flask import request

from visitors_stats.Constants import Constants
from visitors_stats.VisitorsStats import VisitorsStats

app = Flask(__name__)
stats = VisitorsStats({"host": "localhost",
                       "user": "root",
                       "database": "visitors_db",
                       "password": ""})


@app.route(Constants.API_ENDPOINT_NEW_USER, methods=["POST"])
def add_user():
    return 200


@app.route(Constants.API_ENDPOINT_USERS, methods=["GET"])
def get_users():
    page = request.args.get('page', Constants.DEFAULT_PAGE_NUMBER)
    limit = request.args.get('limit', Constants.MAX_USERS_PER_PAGINATED_REQUEST)
    sort_field = request.args.get('field', Constants.DEFAULT_SORT_FIELD)
    sort_order = request.args.get('sort', Constants.DEFAULT_SORT_ORDER)
    return flask.jsonify(stats.get_users(page, limit, sort_field, sort_order))


@app.route("/")
def hello_world():
    return "<h1>HELLO</h1>"
