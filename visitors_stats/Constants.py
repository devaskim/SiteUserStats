import logging


class Constants:

    API_RESULT_OK = "{ 'result': 'ok' }"
    API_RESULT_ERROR = "{ 'result': 'error', 'message': '%s' }"

    API_ENDPOINT_BASE = "/api/v1"
    API_ENDPOINT_USERS = API_ENDPOINT_BASE + "/" + "users"
    API_ENDPOINT_NEW_USER = API_ENDPOINT_USERS + "/" + "new"

    DEFAULT_PAGE_NUMBER = 1
    MAX_USERS_PER_PAGINATED_REQUEST = 30
    DEFAULT_SORT_ORDER = "desc"
    DEFAULT_SORT_FIELD = "id"

    LOG_LEVEL = logging.DEBUG
    LOG_MAX_FILE_SIZE = 5 * 1024 * 1024
    LOG_MAX_FILE_COUNT = 5
    LOGS_DIRECTORY = "logs"
    LOG_FILE = "app.log"
    LOGGER_NAME = "VisitorsStats"

    DB_TABLE_NAME = "visitors"

    DB_TABLE_FIELD_ID = "id"
    DB_TABLE_FIELD_IP = "ip"
    DB_TABLE_FIELD_OS = "os"
    DB_TABLE_FIELD_URL = "url"
    DB_TABLE_FIELD_DURATION = "duration"
    DB_TABLE_FIELD_LANG = "lang"
    DB_TABLE_FIELD_TIMEZONE = "timezone"
    DB_TABLE_FIELD_AGENT = "agent"
    DB_TABLE_FIELD_RESOLUTION = "resolution"

    DB_TABLE_FIELDS = [
        DB_TABLE_FIELD_ID,
        DB_TABLE_FIELD_IP,
        DB_TABLE_FIELD_OS,
        DB_TABLE_FIELD_URL,
        DB_TABLE_FIELD_DURATION,
        DB_TABLE_FIELD_LANG,
        DB_TABLE_FIELD_TIMEZONE,
        DB_TABLE_FIELD_AGENT,
        DB_TABLE_FIELD_RESOLUTION
    ]

    DB_SQL_TABLE_EXISTS = "SELECT COUNT(*) " \
                          "FROM information_schema.tables " \
                          "WHERE table_name = '" + DB_TABLE_NAME + "'"

    DB_SQL_TABLE_CREATE = "CREATE TABLE IF NOT EXISTS " + DB_TABLE_NAME + " (" + \
                          DB_TABLE_FIELD_ID + " INT AUTO_INCREMENT PRIMARY KEY, " + \
                          DB_TABLE_FIELD_IP + " VARCHAR(255), " + \
                          DB_TABLE_FIELD_OS + " VARCHAR(255), " + \
                          DB_TABLE_FIELD_URL + " VARCHAR(255), " + \
                          DB_TABLE_FIELD_DURATION + " INT, " + \
                          DB_TABLE_FIELD_LANG + " VARCHAR(16), " + \
                          DB_TABLE_FIELD_TIMEZONE + " VARCHAR(255), " + \
                          DB_TABLE_FIELD_AGENT + " VARCHAR(512), " + \
                          DB_TABLE_FIELD_RESOLUTION + " VARCHAR(16)" + \
                          ")"

    DB_TABLE_INSERT_NEW_USER = "INSERT INTO " + DB_TABLE_NAME + " " \
                               "(ip, os, url, duration, lang, timezone, agent, resolution)" + " " \
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    DB_TABLE_SELECT_ALL_USERS = "SELECT * FROM " + DB_TABLE_NAME

    DB_TABLE_SELECT_PAGINATED_USERS = "SELECT * " \
                                      "FROM " + DB_TABLE_NAME + " " \
                                      "ORDER BY {0} {1} " \
                                      "LIMIT {2}, {3}"
