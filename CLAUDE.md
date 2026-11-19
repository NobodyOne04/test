# test

A 2019 one-page restaurant website (FC Lokomotiv: HTML, LESS, jQuery, Russian content) with a
hexagonal Python back end for table reservations (ADR 0003).

## Commands
```sh
make install    # uv sync
make run        # site + POST /reservations on 127.0.0.1:8000
make list       # upcoming reservations (CLI)
make check      # ruff check + ruff format --check + pytest (run before every PR)
```
Styles: edit `www/public/less/*.less`, then `npx lessc www/public/less/main.less www/public/css/main.css`.

## Layout
- `www/`: the site (`index.html`, `public/{css,less,js,font,img}`); `main.js` posts the form.
- `src/reservations/core/`: `domain/` (rules), `ports/` (`ReservationStore`, `Clock`),
  `application/` (`ReservationService`). No FastAPI, no SQLite.
- `src/reservations/adapters/`: `outbound/` (`sqlite.py`, `clock.py`), `inbound/` (`http.py`, `cli.py`).
- `src/reservations/composition.py`: wiring; `$RESERVATIONS_DB` picks the database.
- `tests/`: `test_core.py`, `test_sqlite_store.py`, `test_http.py`.
- `trunk/`, `branches/{img,js}`: SVN-style copies from the 2019 exercise, unused.
- `docs/adr/`: decision records (`.adr`), index in `docs/adr/README.md`.

## Conventions
- Read the ADR before changing a recorded decision; commit subjects carry its number.
- Validation lives in `ReservationRequest.validate`; messages are Russian and shown to guests as is.
- Never add an HTTP endpoint that lists reservations without authentication (personal data).
- `www/public/css/main.css` is generated from LESS; don't edit it by hand.
- New rules get a core test with the fixed clock.
