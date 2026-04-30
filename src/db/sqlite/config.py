import sqlite3

DB_PATH = r"\\192.168.11.88\\Projetos\\phd-bi-nps\\nps.db"

sqlite_connection = sqlite3.connect(
    DB_PATH,
    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
)

sqlite_cursor = sqlite_connection.cursor()
