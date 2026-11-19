from datetime import datetime

from reservations.adapters.outbound.sqlite import SqliteReservationStore
from reservations.core.domain import ReservationRequest

GOOD = {"day": "25.11.2026", "time": "19:30", "count": "4", "name": "Анна", "phone": "89001234567"}


def test_round_trip_survives_reopening(tmp_path):
    r = ReservationRequest(**GOOD).validate(datetime(2026, 11, 20, 12, 0))
    SqliteReservationStore(tmp_path / "r.db").add(r)
    assert SqliteReservationStore(tmp_path / "r.db").all() == [r]
