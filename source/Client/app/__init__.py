import os

from flask import Flask
from flask_cors.extension import CORS
from socketio import Client

LIST_RPI = []
IS_EMBEDDED = os.path.isdir("/home/yuri")
SOCKET_CLIENT = Client(reconnection=True)
APP_CORS = CORS()
PIN_RELAY = 16
CWD = os.getcwd()
METADATA_WAIT_TIME = 300  # 5 minutes

if IS_EMBEDDED:
    CONFIG_FILE = "/home/yuri/device_config.json"
    HOME_DIR = "/home/yuri"
else:
    CONFIG_FILE = f"{CWD}/source/Client/device_config.json"
    HOME_DIR = CWD


def create_app():
    app = Flask(__name__)

    APP_CORS.init_app(app)

    if IS_EMBEDDED:
        from .main import gpio_actions

        gpio_actions.gpio_setup()

    from app.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
