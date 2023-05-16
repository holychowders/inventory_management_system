import logging
import sqlite3

from flask import Flask
from flask_login import LoginManager

from . import db, routes
from .db import User


def run() -> None:
    logging.basicConfig(format="[%(levelname)s] %(filename)s %(funcName)s(): %(message)s", level=logging.INFO)

    db.ensure_db()
    flask_app.run(debug=True, host="0.0.0.0", port=8000)


def create_flask_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    # FIXME: Use this only for testing. Do not store secrets in source.
    app.secret_key = "UND2023CSCI455"

    app.register_blueprint(routes.blueprint)

    return app


flask_app = create_flask_app()
login_manager = LoginManager(flask_app)
login_manager.login_view = "blueprint.index"


@login_manager.user_loader  # type: ignore
def load_user(user_id: str) -> User | None:
    with sqlite3.connect(db.DB_PATH) as conn:
        cursor = conn.cursor()
        query = f"SELECT id, username, pin FROM login_credentials WHERE id={user_id}"

        logging.info(query)

        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            user = User(id=result[0], username=result[1], pin=result[2])  # pylint: disable=duplicate-code
            return user
        return None
