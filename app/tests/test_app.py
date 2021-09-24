import sys


def fixPath(path):
    for i in range(2):
        slashIdx = path.rfind("/")
        path = path[:slashIdx]

    return path


sys.path.insert(0, fixPath(sys.path[0]))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    return app.test_client()


def test_get_home(client):
    r = client.get("/")

    if r.status_code != 200:
        raise Exception("Err, status code should be 200")


def test_post_home(client):
    status = "hi"
    r = client.post("/", data=status)

    if r.status_code != 200:
        raise Exception("Err, status code should be 200")


def test_post_status(client):
    r = client.get("/tweet:123")
    print(r)
    print(r.status_code)

    if r.status_code != 200:
        raise Exception("Err, status code should be 200")


def test_status(client):
    r = client.get("/status")

    if r.status_code != 200:
        raise Exception("Err, status code should be 200")


def test_remove_status(client):
    r = client.get("/remove_status:123321")

    print(r.status_code)

    if r.status_code != 302:
        raise Exception("Err, status code should be 200")
