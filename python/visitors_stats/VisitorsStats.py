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
            self.db = mysql.connector.connect(self.db_config)
            self.db_cursor = self.db.cursor()

            if not self._check_db_table():
                self.db_cursor.execute(Constants.DB_TABLE_CREATE_SQL)

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
            self.db_cursor.execute(Constants.DB_TABLE_INSERT_NEW_USER, user)
            self.db.commit()
        except DatabaseError as e:
            # TODO: add this? self.db_is_ok = False
            print("DB insert error: " + e.message)

    def get_users(self, page):
        users = []
        try:

            self.db_cursor.execute(Constants.DB_TABLE_SELECT_ALL_USERS)
            result = self.db_cursor.fetchall()
            for row in result:
                print(row)
                # users.append(row)
        except DatabaseError as e:
            print("DB insert error: " + e.message)
        return users
