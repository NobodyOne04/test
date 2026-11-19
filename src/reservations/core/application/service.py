from reservations.core.domain import Reservation, ReservationRequest
from reservations.core.ports import Clock, ReservationStore


class ReservationService:
    def __init__(self, store: ReservationStore, clock: Clock) -> None:
        self._store = store
        self._clock = clock

    def book(self, request: ReservationRequest) -> Reservation:
        """Validate and store; raises InvalidReservation with per-field messages."""
        reservation = request.validate(self._clock.now())
        self._store.add(reservation)
        return reservation

    def upcoming(self) -> list[Reservation]:
        today = self._clock.now().date()
        return sorted(
            (r for r in self._store.all() if r.day >= today), key=lambda r: (r.day, r.time)
        )
