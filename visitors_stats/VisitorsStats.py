import json

import mysql.connector
from mysql.connector import DatabaseError

from visitors_stats.Constants import Constants


class VisitorsStats:

    def __init__(self, db_config):
        self.db_config = db_config
        self.db = None
        self.db_is_ok = False
        self._init_db()

    def _init_db(self):
        db_cursor = None
        try:
            # For re-init case
            if self.db is not None:
                self.db.close()
                self.db = None

            self.db = mysql.connector.connect(host=self.db_config["host"],
                                              user=self.db_config["user"],
                                              password=self.db_config["password"],
                                              database=self.db_config["database"])
            db_cursor = self.db.cursor()
            db_cursor.execute(Constants.DB_SQL_TABLE_CREATE)
            db_cursor.close()

            self.db_is_ok = True
        except DatabaseError as e:
            self.db_is_ok = False
            print("DB init error: " + e.message)

    def _get_user_count(self):
        if not self.db_is_ok:
            return -1
        db_cursor = self.db.cursor()
        db_cursor.execute(Constants.DB_SQL_USERS_COUNT)
        user_count = db_cursor.fetchone()[0]
        db_cursor.close()
        return user_count

    def add_user(self, data):
        error_response = {
            "result": "error"
        }
        if not self.db_is_ok:
            error_message = "db is not ok, see init phase in logs"
            error_response["message"] = error_message
            print("Skip new user: " + error_message)
            return error_response

        db_cursor = None
        try:
            user = json.loads(data)
            db_cursor = self.db.cursor()
            db_cursor.execute(Constants.DB_SQL_INSERT_NEW_USER,
                              (user.get("ip", ""),
                               user.get("os", ""),
                               user.get("url", ""),
                               user.get("duration", -1),
                               user.get("lang", ""),
                               user.get("timezone", ""),
                               user.get("agent", ""),
                               user.get("resolution", "")))
            self.db.commit()
            db_cursor.close()
            return {"result": "ok"}
        except DatabaseError as e:
            error_response["message"] = e.message
            print("DB user insert error: " + e.message)
            if db_cursor is not None:
                db_cursor.close()
            self._init_db()
            return error_response

    def get_users(self, page, limit, sort_field, sort_order):
        db_cursor = None
        users_count = 0
        users = []

        try:
            users_count = self._get_user_count()
            if users_count == 0:
                return {
                    "page": Constants.DEFAULT_PAGE_NUMBER,
                    "limit": Constants.MAX_USERS_PER_PAGINATED_REQUEST,
                    "total": users_count,
                    "data": users
                }

            current_page = Constants.DEFAULT_PAGE_NUMBER if int(page) < Constants.DEFAULT_PAGE_NUMBER else int(page)
            current_limit = Constants.MAX_USERS_PER_PAGINATED_REQUEST if int(limit) <= 0 else int(limit)
            current_sort_order = sort_order if sort_order == "desc" or sort_order == "asc" else Constants.DB_SQL_DEFAULT_SORTING
            current_sort_field = Constants.DB_TABLE_FIELD_ID
            try:
                if Constants.DB_TABLE_FIELDS.index(sort_field):
                    current_sort_field = sort_field
            except:
                pass

            db_cursor = self.db.cursor()
            db_cursor.execute(Constants.DB_SQL_SELECT_PAGINATED_USERS.format(current_sort_field,
                                                                             current_sort_order,
                                                                             (current_page - 1) * current_limit,
                                                                             current_limit))
            result = db_cursor.fetchall()
            for row in result:
                user = {}
                for i, value in enumerate(row):
                    user[Constants.DB_TABLE_FIELDS[i]] = value
                users.append(user)
            db_cursor.close()
        except DatabaseError as e:
            print("DB users select error: " + e.message)
            if db_cursor is not None:
                db_cursor.close()
            self._init_db()

        return {
            "page": current_page,
            "limit": current_limit,
            "total": users_count,
            "data": users
        }
