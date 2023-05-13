import logging
import sqlite3

from flask import Flask, Response, redirect, render_template, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

import db
from db import Address, Customer, Product, User

flask_app = Flask(__name__, template_folder="../templates", static_folder="../static")
flask_app.secret_key = "UND2023CSCI455"

login_manager = LoginManager(flask_app)
login_manager.login_view = "index"


def main() -> None:
    db.ensure_db()
    flask_app.run(debug=True, host="0.0.0.0", port=8000)


# TODO: Understand how this works, its constraints, and try to simplify it
def format_phone_number(phone_number: str) -> str:
    # Borrowed from:
    #   - "What's the best way to format a phone number in Python?"
    #   - https://stackoverflow.com/a/7058216/13327811
    return format(int(phone_number[:-1]), ",").replace(",", "-") + phone_number[-1]


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


@flask_app.route("/customers")
def customers() -> str:
    customers = []
    for raw_customer in db.all_customers():
        customer = Customer(raw_customer)
        customer.phone = format_phone_number(str(customer.phone))

        if customer.address_id:
            address = db.address(customer.address_id)
            customer.address = Address(address) if address else None
            customers.append(customer)

    return render_template("customers.html", customers=customers)


@flask_app.route("/delete-customer/<int:id>")
def delete_customer(id: int) -> Response:
    db.delete_customer(id)
    return redirect("/customers")  # type: ignore


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


@flask_app.route("/products/add", methods=["POST"])
def add_product() -> Response | str:
    raw_name, raw_description, raw_quantity, raw_price = (
        request.form.get("name"),
        request.form.get("description"),
        request.form.get("quantity_available"),
        request.form.get("price"),
    )

    logging.info(
        """Submitted product addition form. Will validate:
    name: %s
    description: %s
    quantity: %s
    price: %s""",
        repr(raw_name),
        repr(raw_description),
        repr(raw_quantity),
        repr(raw_price),
    )

    # Validate types
    description = raw_description if raw_description else ""
    try:
        name = str(raw_name)
        # FIXME: Numbers such as 5.0 should work
        quantity = int(raw_quantity)  # type: ignore
        price = float(raw_price)  # type: ignore
    except TypeError:
        # TODO: Improve this error message
        error_msg = "One or more required fields were not provided"
        logging.error(error_msg)
        return error_msg
    except ValueError as exception:
        logging.error(str(exception))
        return str(exception)
    else:
        logging.info("Validated types")

    # Validate values
    name = name.strip()
    description = description.strip()
    if not (quantity >= 0 and price >= 0):
        error_msg = "quantity and/or price was less than 0"
        logging.error(error_msg)
        return error_msg
    elif not name:
        error_msg = "name must be provided"
        logging.error(error_msg)
        return error_msg
    else:
        logging.info("Validated values")

    logging.info(
        """Validated and processed product addition form as:
    name: %s
    description: %s
    quantity: %s
    price: %s""",
        repr(name),
        repr(description),
        repr(quantity),
        repr(price),
    )

    new_product = Product((None, name, description, quantity, price))
    logging.info("New product: %s", new_product)
    db.add_product(new_product)

    return redirect("/products")  # type: ignore


@flask_app.route("/products/edit/submit", methods=["POST"])
def submit_product_edit() -> Response | str:
    raw_id, raw_name, raw_description, raw_quantity, raw_price = (
        request.form.get("id"),
        request.form.get("name"),
        request.form.get("description"),
        request.form.get("quantity_available"),
        request.form.get("price"),
    )

    logging.info(
        """Submitted product edit form. Will validate:
    id: %s
    name: %s
    description: %s
    quantity: %s
    price: %s""",
        repr(raw_id),
        repr(raw_name),
        repr(raw_description),
        repr(raw_quantity),
        repr(raw_price),
    )

    # TODO: If couldn't complete request, try redirecting to products edit page so the user can retry
    #   If using `id` to do this, first make sure it's available

    # Validate types
    description = raw_description if raw_description else ""
    try:
        id = int(raw_id)  # type: ignore
        name = str(raw_name)
        # FIXME: Numbers such as 5.0 should work
        quantity = int(raw_quantity)  # type: ignore
        price = float(raw_price)  # type: ignore
    except TypeError:
        error_msg = "One or more required fields were not provided"
        logging.error(error_msg)
        return error_msg
    except ValueError as exception:
        logging.error(str(exception))
        return str(exception)
    else:
        logging.info("Validated types")

    # Validate values
    name = name.strip()
    description = description.strip()
    if not (id >= 0 and quantity >= 0 and price >= 0):
        error_msg = "At least one of id, quantity, or price was less than 0"
        logging.error(error_msg)
        return error_msg
    elif not name:
        error_msg = "name must be provided"
        logging.error(error_msg)
        return error_msg
    else:
        logging.info("Validated values")

    logging.info(
        """Validated and processed product edit form data as:
    id: %s
    name: %s
    description: %s
    quantity: %s
    price: %s""",
        repr(id),
        repr(name),
        repr(description),
        repr(quantity),
        repr(price),
    )

    updated_product = Product((id, name, description, quantity, price))
    logging.info("Product with updates: %s", updated_product)
    db.update_product(updated_product)

    return redirect("/products")  # type: ignore


if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] %(filename)s %(funcName)s(): %(message)s", level=logging.INFO)
    main()
