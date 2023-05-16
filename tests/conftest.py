import pytest
from flask import Flask
from flask.testing import FlaskClient

from ims import create_flask_app, db


@pytest.fixture()
def app() -> Flask:
    app = create_flask_app()
    db.ensure_db()

    return app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()
