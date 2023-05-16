from flask.testing import FlaskClient


def test_login_page(client: FlaskClient) -> None:
    response = client.get("/")
    assert b"<title>Employee Login - Inventory Management System</title>" in response.data
