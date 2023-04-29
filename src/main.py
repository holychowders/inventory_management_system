import logging
from pprint import pformat

from flask import Flask, render_template

from db import all_products, ensure_db

flask_app = Flask(__name__, template_folder="../templates", static_folder="../static")


def main() -> None:
    ensure_db()
    logging.info("Products:\n%s", pformat(all_products()))

    flask_app.run(host="0.0.0.0", port=80)


@flask_app.route("/")  # noqa: vulture
def index() -> str:
    return render_template("index.html")


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    main()
