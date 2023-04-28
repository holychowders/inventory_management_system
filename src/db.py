import sqlite3
from pathlib import Path

CWD = Path.cwd()
DB_PATH = CWD / "ims.db"
SQL_PATH = CWD / "sql/"


ProductEntry = tuple[int, str, str, int, float]


def all_products() -> list[ProductEntry]:
    query = "SELECT * FROM product ORDER BY price DESC"
    with sqlite3.connect(DB_PATH) as db:
        return db.execute(query).fetchall()
