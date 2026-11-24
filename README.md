# test

A one-page website for the **FC Lokomotiv restaurant complex** (Ресторанный комплекс ФК
«Локомотив»), made in 2019 as a front-end and git practice project. The page is in Russian.

> The previous README described a different project (a Go "Work Time Management" service);
> none of that code is in this repo, so it was replaced.

## Run it

```sh
make install     # uv sync: Python 3.12+, FastAPI
make run         # the site and the booking endpoint on http://127.0.0.1:8000
make list        # upcoming reservations
make check       # ruff lint + format check, pytest
```

The map needs a Google Maps key. Opening `www/index.html` directly still shows the page, but
booking needs `make run`.

## Reservations back end

The form posts to `POST /reservations` (form-encoded: `day`, `time`, `count`, `name`, `phone`)
and gets `{"result": 1}` (201) or `{"result": 0, "errors": {field: message}}` (422); the page
shows the messages. Rules: date `ДД.ММ.ГГГГ`, `ДД.ММ` or ISO and not in the past; time `ЧЧ:ММ`
from 10:00 to 23:00; 1-20 guests; a name; a phone of 10-15 digits. Bookings go to SQLite
(`$RESERVATIONS_DB`, default `reservations.db`, git-ignored). They hold names and phone
numbers, so there is no HTTP endpoint that lists them: use `make list`.

Hexagonal, like [personal-ai](https://github.com/NobodyOne04/personal-ai):

```
src/reservations/
  core/
    domain/        Reservation, ReservationRequest.validate(), InvalidReservation
    ports/         ReservationStore, Clock
    application/   ReservationService: book, upcoming
  adapters/
    outbound/      SqliteReservationStore, SystemClock
    inbound/       http.py (FastAPI + the static site), cli.py (list, serve)
  composition.py   reservation_service()
tests/             core (fake store, fixed clock), SQLite store, HTTP (TestClient)
```

## Page

Sections: header (`#section-head`), info, gallery (FlexSlider carousel), reservation form, and
contacts with a map.

## Layout

| Path | What |
|---|---|
| `www/index.html` | the page |
| `www/public/less/` | styles in LESS (`main.less` imports reset, font, btn, layout) |
| `www/public/css/main.css` | the compiled CSS the page loads |
| `www/public/js/main.js` | menu, slider setup, AJAX reservation form (posts to `/reservations`) |
| `www/public/js/lib/` | jQuery FlexSlider |
| `www/public/font/`, `img/` | Exo 2 web fonts, icons, slides |
| `trunk/`, `branches/` | SVN-style copies from the exercise (unminified jQuery and Maps scripts; `img`, `js` variants) |

Decisions: [docs/adr](docs/adr/README.md).
