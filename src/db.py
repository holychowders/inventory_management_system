import sqlite3
from pathlib import Path

CWD = Path.cwd()
DB_PATH = CWD / "ims.db"
SQL_PATH = CWD / "sql/"


ProductEntry = tuple[int, str, str, int, float]


# from dataclasses import dataclass
# @dataclass
# class Product:
#     """
#     Wrapper around database `product` table entries.
#     It aims to simplify the use of product data once pulled from the database.
#
#     Example usage:
#     products = (Product(entry) for entry in db.all_products())
#     for product in products:
#         print(product.id, product.name, product.description, ...)
#     """
#
#     id: int
#     name: str
#     description: str
#     quantity_available: int
#     price: float
#
#     def __init__(self, entry: ProductEntry):
#         self.id = entry[0]
#         self.name = entry[1]
#         self.description = entry[2]
#         self.quantity_available = entry[3]
#         self.price = entry[4]


def all_products() -> list[ProductEntry]:
    query = "SELECT * FROM product ORDER BY price DESC"
    with sqlite3.connect(DB_PATH) as db:
        return db.execute(query).fetchall()
