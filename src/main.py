import logging
import sqlite3

from flask import Flask, Response, redirect, render_template, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

import db
from db import Product, User, ensure_db

flask_app = Flask(__name__, template_folder="../templates", static_folder="../static")
flask_app.secret_key = "UND2023CSCI455"

login_manager = LoginManager(flask_app)
login_manager.login_view = "index"


def main() -> None:
    ensure_db()
    flask_app.run(debug=True, host="0.0.0.0", port=80)


@login_manager.user_loader  # type: ignore
def load_user(user_id: str) -> UserMixin:
    with sqlite3.connect("ims.db") as conn:
        cursor = conn.cursor()
        query = "SELECT id, username, pin FROM login_credentials WHERE id = ?"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            user = User(id=result[0], username=result[1], pin=result[2])
            return user
        return None


@flask_app.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect("/")  # type: ignore


@flask_app.route("/", methods=["GET", "POST"])
def index() -> Response | str:
    if request.method == "POST":
        username = request.form["username"]
        pin = request.form["pin"]

        with sqlite3.connect("ims.db") as conn:
            cursor = conn.cursor()
            query = "SELECT id, username, pin FROM login_credentials WHERE username = ? and pin = ?"
            cursor.execute(query, (username, pin))
            result = cursor.fetchone()

        if result:
            user = User(id=result[0], username=result[1], pin=result[2])
            login_user(user)
            return redirect("/dashboard")  # type: ignore
        return render_template("index.html", error="Invalid username or pin")
    return render_template("index.html")


@flask_app.route("/dashboard")
@login_required  # type: ignore
def dashboard() -> str:
    return render_template("dashboard.html")


@flask_app.route("/products")
@login_required  # type: ignore
def products() -> str:
    products = (Product(product) for product in db.all_products())
    return render_template("products.html", products=products)


@flask_app.route("/delete-product/<int:id>")
@login_required  # type: ignore
def delete_product(id: int) -> Response:
    db.delete_product(id)

    # FIXME: This assumes that we are on the products page to begin with (refreshes).
    # Otherwise, we probably shouldn't be redirecting to it.
    return redirect("/products")  # type: ignore


@flask_app.route("/products/edit/<int:id>")
@login_required  # type: ignore
def edit_product_in_products_page(id: int) -> str:
    products = (Product(product) for product in db.all_products())
    return render_template("products/edit.html", products=products, id=id)


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    main()
