from flask import Blueprint

main = Blueprint("main", __name__)
from . import events, methods, routes

main_package = {
    "routes": routes,
    "socket": events,
    "methods": methods,
}
