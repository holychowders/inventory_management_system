import logging

from flask import Flask, Response, redirect, render_template, request

import db
from db import Product

flask_app = Flask(__name__, template_folder="../templates", static_folder="../static")


def main() -> None:
    db.ensure_db()
    flask_app.run(debug=True, host="0.0.0.0", port=80)


@flask_app.route("/")
def index() -> str:
    return render_template("index.html")


@flask_app.route("/dashboard")
def dashboard() -> str:
    return render_template("dashboard.html")


@flask_app.route("/products")
def products() -> str:
    products = (Product(product) for product in db.all_products())
    return render_template("products.html", products=products)


@flask_app.route("/delete-product/<int:id>")
def delete_product(id: int) -> Response:
    db.delete_product(id)

    # FIXME: This assumes that we are on the products page to begin with (refreshes).
    # Otherwise, we probably shouldn't be redirecting to it.
    return redirect("/products")  # type: ignore


@flask_app.route("/products/edit/<int:id>")
def edit_product_in_products_page(id: int) -> str:
    products = (Product(product) for product in db.all_products())
    return render_template("products/edit.html", products=products, id=id)


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
        """
    Submitted product edit. Will validate:
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
        """
    Validated and processed product edit submission data as:
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

    new_product = Product((id, name, description, quantity, price))
    db.update_product(new_product)

    return redirect("/products")  # type: ignore


if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] %(filename)s %(funcName)s(): %(message)s", level=logging.INFO)
    main()
