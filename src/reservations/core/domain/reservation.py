import re
from dataclasses import dataclass
from datetime import date, datetime, time

OPENS, CLOSES = time(10, 0), time(23, 0)
MAX_GUESTS = 20
_PHONE_CHARS = re.compile(r"[\s()\-]")


class InvalidReservation(ValueError):
    """The request breaks one or more rules; errors maps field → message (Russian, shown as is)."""

    def __init__(self, errors: dict[str, str]) -> None:
        super().__init__(errors)
        self.errors = errors


@dataclass(frozen=True)
class Reservation:
    day: date
    time: time
    guests: int
    name: str
    phone: str
    created_at: datetime


@dataclass(frozen=True)
class ReservationRequest:
    """What the form sends: free text, as typed."""

    day: str = ""
    time: str = ""
    count: str = ""
    name: str = ""
    phone: str = ""

    def validate(self, now: datetime) -> Reservation:
        errors: dict[str, str] = {}
        day = _day(self.day.strip(), now.date(), errors)
        at = _time(self.time.strip(), errors)
        guests = _guests(self.count.strip(), errors)
        name = self.name.strip()
        if not 1 <= len(name) <= 100:
            errors["name"] = "Укажите имя (до 100 символов)."
        phone = _phone(self.phone.strip(), errors)
        if errors:
            raise InvalidReservation(errors)
        return Reservation(day, at, guests, name, phone, now)  # type: ignore[arg-type]


def _day(raw: str, today: date, errors: dict[str, str]) -> date | None:
    if re.fullmatch(r"\d{1,2}\.\d{1,2}", raw):  # ДД.ММ means this year
        raw = f"{raw}.{today.year}"
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
        if parsed < today:
            errors["day"] = "Дата уже прошла."
            return None
        return parsed
    errors["day"] = "Дата в формате ДД.ММ.ГГГГ."
    return None


def _time(raw: str, errors: dict[str, str]) -> time | None:
    try:
        parsed = datetime.strptime(raw.replace(".", ":"), "%H:%M").time()
    except ValueError:
        errors["time"] = "Время в формате ЧЧ:ММ."
        return None
    if not OPENS <= parsed <= CLOSES:
        errors["time"] = f"Мы работаем с {OPENS:%H:%M} до {CLOSES:%H:%M}."
        return None
    return parsed


def _guests(raw: str, errors: dict[str, str]) -> int | None:
    if raw.isdigit() and 1 <= int(raw) <= MAX_GUESTS:
        return int(raw)
    errors["count"] = f"Количество гостей от 1 до {MAX_GUESTS}."
    return None


def _phone(raw: str, errors: dict[str, str]) -> str | None:
    digits = _PHONE_CHARS.sub("", raw).removeprefix("+")
    if digits.isdigit() and 10 <= len(digits) <= 15:
        return "+" + digits
    errors["phone"] = "Телефон: 10-15 цифр."
    return None
