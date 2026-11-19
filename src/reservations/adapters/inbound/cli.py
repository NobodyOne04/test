"""CLI adapter: `reservations list` prints upcoming bookings; `reservations serve` runs the site."""

import argparse

from reservations import composition


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="reservations")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="upcoming reservations")
    serve = sub.add_parser("serve", help="run the site and the booking endpoint")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    if args.command == "list":
        upcoming = composition.reservation_service().upcoming()
        for r in upcoming:
            print(f"{r.day:%d.%m.%Y} {r.time:%H:%M}  {r.guests:>2} гост.  {r.name}  {r.phone}")
        if not upcoming:
            print("Нет предстоящих бронирований.")
    else:
        import uvicorn

        uvicorn.run("reservations.adapters.inbound.http:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
