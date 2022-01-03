import mysql.connector
from mysql.connector import DatabaseError

from visitors_stats.Constants import Constants


class VisitorsStats:

    def __init__(self, db_config):
        self.db_config = db_config
        self.db = None
        self.db_cursor = None
        self.db_is_ok = False
        self._init_db()

    def _check_db_table(self):
        return self.db_cursor.execute(Constants.DB_SQL_TABLE_EXISTS).fetchone()[0] == 1

    def _init_db(self):
        try:
            self.db = mysql.connector.connect(host=self.db_config["host"],
                                              user=self.db_config["user"],
                                              password=self.db_config["password"],
                                              database=self.db_config["database"])
            self.db_cursor = self.db.cursor()
            self.db_cursor.execute(Constants.DB_SQL_TABLE_CREATE)
            self.db_is_ok = True
        except DatabaseError as e:
            self.db_is_ok = False
            print("DB init error: " + e.message)

    def add_user(self, user):
        if not self.db_is_ok:
            error_message = "db is not ok, see init phase in logs"
            print("Skip new user: " + error_message)
            return Constants.API_RESULT_ERROR.format(error_message)

        try:
            self.db_cursor.execute(Constants.DB_TABLE_INSERT_NEW_USER, (user["ip"], user["os"]))
            self.db.commit()
        except DatabaseError as e:
            print("DB user insert error: " + e.message)

    def get_users(self, page, limit, sort_field, sort_order):
        users = []
        try:
            current_page = Constants.DEFAULT_PAGE_NUMBER if int(page) < Constants.DEFAULT_PAGE_NUMBER else int(page)
            current_limit = Constants.MAX_USERS_PER_PAGINATED_REQUEST if int(limit) <= 0 else int(limit)
            self.db_cursor.execute(Constants.DB_TABLE_SELECT_PAGINATED_USERS.format(sort_field,
                                                                                    sort_order,
                                                                                    (current_page - 1) * current_limit,
                                                                                    current_limit))
            result = self.db_cursor.fetchall()
            for row in result:
                users.append({"id": row[0], "ip": row[1], "os": row[2]})
        except DatabaseError as e:
            print("DB users select error: " + e.message)
        return users
