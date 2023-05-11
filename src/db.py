import logging
import sqlite3
from dataclasses import dataclass
from pathlib import Path

CWD = Path.cwd()
DB_PATH = CWD / "ims.db"
SQL_PATH = CWD / "sql/"


ProductEntry = tuple[int | None, str, str, int, float]


@dataclass
class Product:
    """
    Wrapper around database `product` table entries.
    It aims to simplify the use of product data once pulled from the database.

    Example usage:
    products = (Product(entry) for entry in db.all_products())
    for product in products:
        print(product.id, product.name, product.description, ...)
    """

    # Can be `None` if is a new product rather than updating an existing product
    id: int | None
    name: str
    description: str
    quantity_available: int
    price: float

    def __init__(self, entry: ProductEntry):
        self.id = entry[0]
        self.name = entry[1]
        self.description = entry[2]
        self.quantity_available = entry[3]
        self.price = entry[4]


def ensure_db() -> None:
    if DB_PATH.exists():
        logging.info("Database file found: %s", DB_PATH)
    else:
        logging.warning("Database file not found. Creating %s", DB_PATH)
        # Connecting creates the database file if it doesn't exist.
        with sqlite3.connect(DB_PATH) as db:
            logging.info("Database file created: %s", DB_PATH)

            create_tables_sql_path = SQL_PATH / "create_tables.sql"
            logging.info("Creating tables with %s", create_tables_sql_path)
            with open(create_tables_sql_path, encoding="utf-8") as script:
                db.executescript(script.read())
                logging.info("Created tables")

            logging.info("Populating database")
            population_script_paths = SQL_PATH.glob("populate_sample_data/*")
            for script_path in population_script_paths:
                logging.info("Populating database with %s", script_path)
                with open(script_path, encoding="utf-8") as script:
                    db.executescript(script.read())
            logging.info("Populated database")


def add_product(product: Product) -> None:
    if product.id is not None:
        logging.warning("id should not be present adding new product. Is something wrong?")

    sql = f"""
    INSERT INTO product (name, description, quantity_available, price)
    VALUES ('{product.name}', '{product.description}', {product.quantity_available}, {product.price})"""

    logging.info("%s", sql)

    with sqlite3.connect(DB_PATH) as db:
        db.execute(sql)


def update_product(product: Product) -> None:
    if not product.id:
        logging.error("Can't update product without id: %s", product)
        return

    sql = f"""
    UPDATE product SET
    name='{product.name}',
    description='{product.description}',
    quantity_available={product.quantity_available},
    price={product.price}
    WHERE id={product.id}"""

    logging.info("%s", sql)

    with sqlite3.connect(DB_PATH) as db:
        db.execute(sql)


def all_products() -> list[ProductEntry]:
    query = "SELECT * FROM product ORDER BY price DESC"
    with sqlite3.connect(DB_PATH) as db:
        return db.execute(query).fetchall()


def delete_product(id: int) -> None:
    with sqlite3.connect(DB_PATH) as db:
        sql = f"DELETE FROM product WHERE id={id}"
        db.execute(sql)
