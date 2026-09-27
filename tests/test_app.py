import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["service"] == "meridian-pay"


def test_echo(client):
    resp = client.post("/api/echo", json={"hello": "world"})
    assert resp.status_code == 200
    assert resp.get_json() == {"received": {"hello": "world"}}


def test_echo_empty_body(client):
    resp = client.post("/api/echo")
    assert resp.status_code == 200
    assert resp.get_json() == {"received": {}}
