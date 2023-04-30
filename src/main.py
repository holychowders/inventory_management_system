import logging

from flask import Flask, Response, redirect, render_template

import db
from db import Product, ensure_db

flask_app = Flask(__name__, template_folder="../templates", static_folder="../static")


def main() -> None:
    ensure_db()
    flask_app.run(host="0.0.0.0", port=80)


@flask_app.route("/")
def index() -> str:
    return render_template("index.html")


@flask_app.route("/dashboard")
def dashboard() -> str:
    return render_template("dashboard.html")


@flask_app.route("/products")
def products() -> str:
    products = (Product(product) for product in db.all_products())  # pylint: disable=redefined-outer-name
    return render_template("products.html", products=products)


@flask_app.route("/delete-product/<int:id>")
def delete_product(id: int) -> Response:  # pylint: disable=redefined-builtin
    db.delete_product(id)

    # FIXME: This assumes that we are on the products page to begin with (refreshes).
    # Otherwise, we probably shouldn't be redirecting to it.
    return redirect("/products")  # type: ignore


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    main()
