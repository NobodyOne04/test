import sqlite3
from datetime import date, datetime, time
from pathlib import Path

from reservations.core.domain import Reservation

_SCHEMA = """
CREATE TABLE IF NOT EXISTS reservations (
    id         INTEGER PRIMARY KEY,
    day        TEXT NOT NULL,
    time       TEXT NOT NULL,
    guests     INTEGER NOT NULL,
    name       TEXT NOT NULL,
    phone      TEXT NOT NULL,
    created_at TEXT NOT NULL
)
"""


class SqliteReservationStore:
    """ReservationStore in one SQLite file; a connection per call keeps it thread-safe."""

    def __init__(self, path: Path) -> None:
        self._path = path
        with self._connect() as db:
            db.execute(_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path)

    def add(self, r: Reservation) -> None:
        with self._connect() as db:
            db.execute(
                "INSERT INTO reservations (day, time, guests, name, phone, created_at)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (
                    r.day.isoformat(),
                    r.time.isoformat("minutes"),
                    r.guests,
                    r.name,
                    r.phone,
                    r.created_at.isoformat(),
                ),
            )

    def all(self) -> list[Reservation]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT day, time, guests, name, phone, created_at FROM reservations ORDER BY id"
            ).fetchall()
        return [
            Reservation(
                date.fromisoformat(d), time.fromisoformat(t), g, n, p, datetime.fromisoformat(c)
            )
            for d, t, g, n, p, c in rows
        ]
