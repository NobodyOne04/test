"""Composition root: the only place that picks adapters."""

import os
from functools import cache
from pathlib import Path

from reservations.adapters.outbound.clock import SystemClock
from reservations.adapters.outbound.sqlite import SqliteReservationStore
from reservations.core.application import ReservationService

REPO = Path(__file__).resolve().parents[2]
SITE = REPO / "www"


@cache
def reservation_service() -> ReservationService:
    db = Path(os.environ.get("RESERVATIONS_DB", REPO / "reservations.db"))
    return ReservationService(SqliteReservationStore(db), SystemClock())
