"""FastAPI adapter: the booking endpoint plus the static site."""

from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from reservations import composition
from reservations.core.domain import InvalidReservation, ReservationRequest


def create_app() -> FastAPI:
    app = FastAPI(title="Restaurant reservations", docs_url=None, redoc_url=None)

    @app.post("/reservations")
    def book(
        day: Annotated[str, Form()] = "",
        time: Annotated[str, Form()] = "",
        count: Annotated[str, Form()] = "",
        name: Annotated[str, Form()] = "",
        phone: Annotated[str, Form()] = "",
    ) -> JSONResponse:
        request = ReservationRequest(day=day, time=time, count=count, name=name, phone=phone)
        try:
            composition.reservation_service().book(request)
        except InvalidReservation as invalid:
            return JSONResponse({"result": 0, "errors": invalid.errors}, status_code=422)
        return JSONResponse({"result": 1}, status_code=201)

    # last, so /reservations wins over the static files
    app.mount("/", StaticFiles(directory=composition.SITE, html=True), name="site")
    return app


app = create_app()
