import sqlite3

from src.config import CONFIGS

DB_PATH = CONFIGS.get("SQLITE_DB_PATH")

sqlite_connection = sqlite3.connect(
    DB_PATH,
    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
)

sqlite_cursor = sqlite_connection.cursor()
