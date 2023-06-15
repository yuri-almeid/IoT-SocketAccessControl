from flask import Blueprint

main = Blueprint("main", __name__)

from . import events, gpio_actions, methods, routes  # noqa

main_package = {
    "methods": methods,
    "routes": routes,
    "socket": events,
    "gpio_actions": gpio_actions,
}
