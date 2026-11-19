# Changelog

## Unreleased

### Added
- Reservations back end (ADR 0003): the form now books tables. Hexagonal core with validation, SQLite storage, FastAPI serving the site and `POST /reservations`, a `reservations list` CLI; uv, ruff, pytest

### Fixed
- The reservation form posted to an `index.php` that never existed, so every booking failed; it now posts to `/reservations` and shows field errors

### Added
- CLAUDE.md, changelog and ADRs

### Changed
- README rewritten: it described an unrelated Go service; it now describes the restaurant site
- Default branch renamed from `master` to `main`
