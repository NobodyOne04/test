"""The FastAPI adapter, on a temporary database."""

from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from reservations import composition


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("RESERVATIONS_DB", str(tmp_path / "r.db"))
    composition.reservation_service.cache_clear()
    from reservations.adapters.inbound.http import create_app

    yield TestClient(create_app())
    composition.reservation_service.cache_clear()


def form(**overrides):
    tomorrow = (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    data = {"day": tomorrow, "time": "19:00", "count": "2", "name": "Иван", "phone": "+79001234567"}
    return {**data, **overrides}


def test_booking(client):
    response = client.post("/reservations", data=form())
    assert response.status_code == 201 and response.json() == {"result": 1}
    assert len(composition.reservation_service().upcoming()) == 1


def test_invalid_booking_lists_errors(client):
    response = client.post("/reservations", data=form(count="0", phone="1"))
    assert response.status_code == 422
    assert response.json()["result"] == 0
    assert set(response.json()["errors"]) == {"count", "phone"}


def test_the_site_is_served(client):
    page = client.get("/")
    assert page.status_code == 200 and "reserve-form" in page.text
    assert "/reservations" in client.get("/public/js/main.js").text


def test_bookings_are_not_listed_over_http(client):
    client.post("/reservations", data=form())
    response = client.get("/reservations")
    assert response.status_code in (404, 405) and "Иван" not in response.text
