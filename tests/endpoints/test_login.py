from flask.testing import FlaskClient

VALID_USERNAME = "agarcia"
VALID_PIN = 5879


def test_load_page(client: FlaskClient) -> None:
    response = client.get("/")
    assert b"<title>Employee Login - Inventory Management System</title>" in response.data


def test_valid_input(client: FlaskClient) -> None:
    data = {"username": VALID_USERNAME, "pin": VALID_PIN}
    response = client.post("/", data=data, follow_redirects=True)
    assert b"<title>Dashboard - Inventory Management System</title>" in response.data


def test_empty_input(client: FlaskClient) -> None:
    data = {"username": "", "pin": ""}
    # NOTE: This assumes that the source of the request did not come from the web page,
    #   and thus that empty input will not have been converted from `""` to `None`
    response = client.post("/", data=data, follow_redirects=True)
    assert (
        b"<title>Employee Login - Inventory Management System</title>" in response.data
    ), "Should remain on login page and reject login"


def test_invalid_username_valid_pin(client: FlaskClient) -> None:
    data = {"username": "some invalid username", "pin": VALID_PIN}
    response = client.post("/", data=data, follow_redirects=True)
    assert (
        b"<title>Employee Login - Inventory Management System</title>" in response.data
    ), "Should remain on login page and reject login"


def test_invalid_username_no_pin(client: FlaskClient) -> None:
    data = {"username": "some invalid username", "pin": ""}
    response = client.post("/", data=data, follow_redirects=True)
    assert (
        b"<title>Employee Login - Inventory Management System</title>" in response.data
    ), "Should remain on login page and reject login"


def test_valid_username_invalid_pin(client: FlaskClient) -> None:
    data = {"username": VALID_USERNAME, "pin": "0000"}
    response = client.post("/", data=data, follow_redirects=True)
    assert (
        b"<title>Dashboard - Inventory Management System</title>" in response.data
    ), "Should remain on login page and reject login"


def test_no_username_invalid_pin(client: FlaskClient) -> None:
    data = {"username": "", "pin": "0000"}
    response = client.post("/", data=data, follow_redirects=True)
    assert (
        b"<title>Dashboard - Inventory Management System</title>" in response.data
    ), "Should remain on login page and reject login"
