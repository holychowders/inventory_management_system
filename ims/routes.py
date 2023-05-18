import logging
import sqlite3

from flask import Blueprint, Response, redirect, render_template, request
from flask_login import login_required, login_user, logout_user

from . import db
from .db import Address, Customer, Product, ProductEntry, User
from .utils import format_phone_number

blueprint = Blueprint("blueprint", __name__, template_folder="../templates", static_folder="../static")


@blueprint.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect("/")  # type: ignore[return-value]


@blueprint.route("/", methods=["GET", "POST"])
def index() -> Response | str:
    if request.method == "POST":
        username = request.form["username"]
        pin = request.form["pin"]

        with sqlite3.connect(db.DB_PATH) as conn:
            cursor = conn.cursor()
            query = f"""SELECT id, username, pin
            FROM login_credentials
            WHERE username='{username}' and pin={pin}
            """  # noqa: S608

            logging.info(query)

            cursor.execute(query)
            result = cursor.fetchone()

        if result:
            user = User(id=result[0], username=result[1], pin=result[2])
            login_user(user)
            return redirect("/dashboard")  # type: ignore[return-value]
        return render_template("index.html", error="Invalid username or pin")
    return render_template("index.html")


@blueprint.route("/dashboard")
@login_required  # type: ignore[misc]
def dashboard() -> str:
    return render_template("dashboard.html")


@blueprint.route("/customers")
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


@blueprint.route("/delete-customer/<int:id>")
def delete_customer(id: int) -> Response:
    db.delete_customer(id)
    return redirect("/customers")  # type: ignore[return-value]


@blueprint.route("/products")
@login_required  # type: ignore[misc]
def products() -> str:
    products = (Product(product) for product in db.all_products())
    return render_template("products.html", products=products)


@blueprint.route("/delete-product/<int:id>")
@login_required  # type: ignore[misc]
def delete_product(id: int) -> Response:
    db.delete_product(id)

    # FIXME: This assumes that we are on the products page to begin with (refreshes).
    # Otherwise, we probably shouldn't be redirecting to it.
    return redirect("/products")  # type: ignore[return-value]


@blueprint.route("/products/edit/<int:id>")
@login_required  # type: ignore[misc]
def edit_product_in_products_page(id: int) -> str:
    products = (Product(product) for product in db.all_products())
    return render_template("products/edit.html", products=products, id=id)


@blueprint.route("/products/add", methods=["POST"])
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
        quantity = int(raw_quantity)  # type: ignore[arg-type]
        price = float(raw_price)  # type: ignore[arg-type]
    except TypeError:
        # TODO: Improve this error message
        error_msg = "One or more required fields were not provided"
        logging.exception(error_msg)
        return error_msg
    except ValueError as exception:
        logging.exception(msg=exception)
        return str(exception)
    else:
        logging.info("Validated types")

    # Validate values
    name = name.strip()
    description = description.strip()
    if not (quantity >= 0 and price >= 0):
        error_msg = "quantity and/or price was less than 0"
        logging.exception(error_msg)
        return error_msg
    elif not name:
        error_msg = "name must be provided"
        logging.exception(error_msg)
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

    new_product = Product(ProductEntry((None, name, description, quantity, price)))
    logging.info("New product: %s", new_product)
    db.add_product(new_product)

    return redirect("/products")  # type: ignore[return-value]


@blueprint.route("/products/edit/submit", methods=["POST"])
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
        id = int(raw_id)  # type: ignore[arg-type]
        name = str(raw_name)
        # FIXME: Numbers such as 5.0 should work
        quantity = int(raw_quantity)  # type: ignore[arg-type]
        price = float(raw_price)  # type: ignore[arg-type]
    except TypeError:
        error_msg = "One or more required fields were not provided"
        logging.exception(error_msg)
        return error_msg
    except ValueError as exception:
        logging.exception(msg=exception)
        return str(exception)
    else:
        logging.info("Validated types")

    # Validate values
    name = name.strip()
    description = description.strip()
    if not (id >= 0 and quantity >= 0 and price >= 0):
        error_msg = "At least one of id, quantity, or price was less than 0"
        logging.exception(error_msg)
        return error_msg
    elif not name:
        error_msg = "name must be provided"
        logging.exception(error_msg)
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

    updated_product = Product(ProductEntry((id, name, description, quantity, price)))
    logging.info("Product with updates: %s", updated_product)
    db.update_product(updated_product)

    return redirect("/products")  # type: ignore[return-value]
