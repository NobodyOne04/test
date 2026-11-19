"""Domain rules and the service, with a fake store and a fixed clock."""

from datetime import date, datetime, time

import pytest

from reservations.core.application import ReservationService
from reservations.core.domain import InvalidReservation, ReservationRequest

NOW = datetime(2026, 11, 20, 12, 0)
GOOD = {
    "day": "25.11.2026",
    "time": "19:30",
    "count": "4",
    "name": "Анна",
    "phone": "+7 (900) 123-45-67",
}


class FixedClock:
    def now(self):
        return NOW


class MemoryStore:
    def __init__(self):
        self.items = []

    def add(self, r):
        self.items.append(r)

    def all(self):
        return list(self.items)


def test_a_valid_request_is_normalised():
    r = ReservationRequest(**GOOD).validate(NOW)
    assert (r.day, r.time, r.guests, r.name, r.phone) == (
        date(2026, 11, 25),
        time(19, 30),
        4,
        "Анна",
        "+79001234567",
    )


@pytest.mark.parametrize(
    "day, expected", [("2026-11-25", date(2026, 11, 25)), ("25.11", date(2026, 11, 25))]
)
def test_other_day_formats(day, expected):
    assert ReservationRequest(**{**GOOD, "day": day}).validate(NOW).day == expected


@pytest.mark.parametrize(
    "field, value",
    [
        ("day", "19.11.2026"),  # past
        ("day", "завтра"),
        ("time", "09:00"),  # before opening
        ("time", "23:30"),
        ("time", "7pm"),
        ("count", "0"),
        ("count", "21"),
        ("count", "четыре"),
        ("name", "  "),
        ("phone", "12345"),
        ("phone", "+7 900 abc"),
    ],
)
def test_each_rule_reports_its_field(field, value):
    with pytest.raises(InvalidReservation) as caught:
        ReservationRequest(**{**GOOD, field: value}).validate(NOW)
    assert list(caught.value.errors) == [field]


def test_all_errors_at_once():
    with pytest.raises(InvalidReservation) as caught:
        ReservationRequest().validate(NOW)
    assert set(caught.value.errors) == {"day", "time", "count", "name", "phone"}


def test_service_books_and_lists_upcoming_in_order():
    store = MemoryStore()
    service = ReservationService(store, FixedClock())
    service.book(ReservationRequest(**{**GOOD, "day": "30.11.2026"}))
    service.book(ReservationRequest(**GOOD))
    assert [r.day.day for r in service.upcoming()] == [25, 30]


def test_service_stores_nothing_when_invalid():
    store = MemoryStore()
    with pytest.raises(InvalidReservation):
        ReservationService(store, FixedClock()).book(ReservationRequest(**{**GOOD, "count": "0"}))
    assert store.items == []
