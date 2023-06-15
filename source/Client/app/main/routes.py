from app import IS_EMBEDDED
from flask import Response

from . import main


@main.route("/status")
def status():
    return Response(
        response={},
        status=200,
        mimetype="application/json",
    )


@main.route("/open")
def open():
    if IS_EMBEDDED:
        main.gpio_actions.open_door()
    else:
        print("[Flask thread] : Door opened in debug mode")

    return Response(
        response={"data": "Success"},
        status=200,
        mimetype="application/json",
    )
