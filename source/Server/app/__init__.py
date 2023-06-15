from datetime import datetime
from threading import Lock

from engineio.payload import Payload
from flask import Flask
from flask_cors.extension import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


EXECUTION_START_TIME = datetime.now()

LIST_RPI = []


THREAD_LOCK = Lock()
THREAD = None
APP_CORS = CORS()
SOCKETIO = SocketIO()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.DevelopmentConfig")

    Payload.max_decode_packets = 50

    APP_CORS.init_app(app)
    SOCKETIO.init_app(app, async_mode=None, ping_timeout=60)

    DB.init_app(app)

    from .models import Device, Logs, Status, Store, User  # noqa

    with app.app_context():
        DB.create_all()

    print("Servidor Iniciado")

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
