from datetime import datetime
from typing import Protocol

from reservations.core.domain import Reservation


class ReservationStore(Protocol):
    def add(self, reservation: Reservation) -> None: ...

    def all(self) -> list[Reservation]: ...


class Clock(Protocol):
    def now(self) -> datetime: ...
