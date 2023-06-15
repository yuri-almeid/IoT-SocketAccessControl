from datetime import datetime

from flask import copy_current_request_context, request, session
from flask_socketio import (  # noqa
    close_room,
    disconnect,
    emit,
    join_room,
    leave_room,
    rooms,
)

from .. import SOCKETIO, THREAD, THREAD_LOCK  # noqa
from . import methods


@SOCKETIO.event
def update(_):
    methods.update_dashboard()
    print("Lista atualizada")


@SOCKETIO.event
def on_list_update(data):
    if data["code"] is not None:
        print("Código: " + data["code"])
        print("Horário: " + str(datetime.now()))

        rpi = {"sid": request.sid, "code": data["code"]}

        methods.create_device(data)

        methods.list_update("connect", rpi)


@SOCKETIO.event
def send_cmd(message):
    emit("command_event", {"data": message["data"]}, to=message["room"])


@SOCKETIO.event
def get_rasp_output(message):
    emit("get_output", {"out": message["out"]}, to=message["room"])


@SOCKETIO.event
def my_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {
            "data": message["data"],
            "count": session["receive_count"],
        },
    )


@SOCKETIO.event
def my_broadcast_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": message["data"], "count": session["receive_count"]},
        broadcast=True,
    )


@SOCKETIO.event
def join(message):
    print("Raspberry Pi: " + message["room"] + " OK")
    print("")
    join_room(message["room"])
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {
            "data": "In rooms: " + ", ".join(rooms()),
            "count": session["receive_count"],
        },
    )


@SOCKETIO.event
def leave(message):
    leave_room(message["room"])
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {
            "data": "In rooms: " + ", ".join(rooms()),
            "count": session["receive_count"],
        },
    )


@SOCKETIO.on("close_room")
def on_close_room(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {
            "data": "Room " + message["room"] + " is closing.",
            "count": session["receive_count"],
        },
        to=message["room"],
    )
    close_room(message["room"])


@SOCKETIO.event
def my_room_event(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": message["data"], "count": session["receive_count"]},
        to=message["room"],
    )


@SOCKETIO.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": "Disconnected!", "count": session["receive_count"]},
        callback=can_disconnect,
    )


@SOCKETIO.event
def my_ping():
    emit("my_pong")


@SOCKETIO.event
def connect():
    global THREAD
    with THREAD_LOCK:
        if THREAD is None:
            THREAD = SOCKETIO.start_background_task(methods.background_thread)
    emit("my_response", {"data": "Connected", "count": 0})


@SOCKETIO.on("connect")
def test_connect():
    print("Novo Cliente Conectado")
    print("SID:", request.sid)
    emit("my_response", {"data": "Connected"})


@SOCKETIO.on("disconnect")
def test_disconnect():
    print("Cliente Desconectado:", request.sid)
    methods.list_update("disconnect", request.sid)
