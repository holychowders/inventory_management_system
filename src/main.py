import logging
import sqlite3
from pathlib import Path

CWD = Path.cwd()
DB_PATH = CWD / "ims.db"
SQL_PATH = CWD / "sql/"


def main() -> None:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

    if DB_PATH.exists():
        logging.info("Database file found: %s", DB_PATH)
    else:
        logging.warning("Database file not found. Creating %s", DB_PATH)
        # Connecting creates the database file if it doesn't exist.
        with sqlite3.connect(DB_PATH) as db:
            logging.info("Database file created: %s", DB_PATH)
            with open(SQL_PATH / "create_tables.sql", encoding="utf-8") as script:
                db.executescript(script.read())
                db.commit()
                logging.info("Created tables")

            logging.info("Populating database")
            population_script_paths = SQL_PATH.glob("populate_sample_data/*")
            for script_path in population_script_paths:
                logging.info("Populating database with %s", script_path)
                with open(script_path, encoding="utf-8") as script:
                    db.executescript(script.read())
                    db.commit()
            logging.info("Populated database")


if __name__ == "__main__":
    main()
