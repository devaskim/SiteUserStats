import logging


class Constants:

    API_RESULT_OK = "{ 'result': 'ok' }"
    API_RESULT_ERROR = "{ 'result': 'error', 'message': '%s' }"

    API_ENDPOINT_BASE = "/v1/api"
    API_ENDPOINT_USERS = API_ENDPOINT_BASE + "/" + "users"
    API_ENDPOINT_NEW_USER = API_ENDPOINT_USERS + "/" + "new"

    LOG_LEVEL = logging.DEBUG
    LOG_MAX_FILE_SIZE = 5 * 1024 * 1024
    LOG_MAX_FILE_COUNT = 5
    LOGS_DIRECTORY = "logs"
    LOG_FILE = "app.log"
    LOGGER_NAME = "VisitorsStats"

    DB_TABLE_NAME = "visitors"

    DB_SQL_TABLE_EXISTS = "SELECT COUNT(*) " \
                          "FROM information_schema.tables " \
                          "WHERE table_name = '" + DB_TABLE_NAME + "'"

    DB_SQL_TABLE_CREATE = "CREATE TABLE " + DB_TABLE_NAME + " (" \
                          "id INT AUTO_INCREMENT PRIMARY KEY, " \
                          "ip VARCHAR(255), " \
                          "os VARCHAR(255)" \
                          ")"

    DB_TABLE_INSERT_NEW_USER = "INSERT INTO " + DB_TABLE_NAME + " (ip, os) VALUES (%s, %s)"
    DB_TABLE_SELECT_ALL_USERS = "SELECT * FROM " + DB_TABLE_NAME
