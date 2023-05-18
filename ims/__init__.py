import logging
import sqlite3

from flask import Flask
from flask_login import LoginManager

from . import db, routes
from .db import User


def run() -> None:
    logging.basicConfig(format="[%(levelname)s] %(filename)s %(funcName)s(): %(message)s", level=logging.INFO)

    db.ensure_db()
    create_flask_app().run(debug=True, host="127.0.0.1")


def create_flask_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    # FIXME: Use this only for testing. Do not store secrets in source.
    app.secret_key = "UND2023CSCI455"  # noqa: S105

    app.register_blueprint(routes.blueprint)

    login_manager = LoginManager(app)
    login_manager.login_view = "blueprint.index"

    @login_manager.user_loader  # type: ignore[misc]
    def load_user(user_id: str) -> User | None:
        with sqlite3.connect(db.DB_PATH) as conn:
            cursor = conn.cursor()
            query = f"SELECT id, username, pin FROM login_credentials WHERE id={user_id}"  # noqa: S608

            logging.info(query)

            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return User(id=result[0], username=result[1], pin=result[2])
            return None

    return app
