import threading

from app import SOCKET_CLIENT, main
from app.main import methods


@SOCKET_CLIENT.event
def connect():
    config = main.methods.load_from_device_config()

    code = config["code"]
    status = SOCKET_CLIENT.eio.state
    connection_type = SOCKET_CLIENT.eio.current_transport
    sid = SOCKET_CLIENT.sid

    print("[Socket thread] : Connected")
    print("[Socket thread] : Device Code: " + code)
    print("[Socket thread] : Status: " + status)
    print("[Socket thread] : Connection Type: " + connection_type)
    print("[Socket thread] : Session ID: " + sid)

    SOCKET_CLIENT.emit(
        "on_list_update",
        {
            "code": config["code"],
            "ip": config["ip"],
            "store_id": config["store_id"],
        },
    )

    SOCKET_CLIENT.emit("join", {"room": config["code"]})

    metadata_thread = threading.Thread(target=methods.device_metadata)
    metadata_thread.start()


@SOCKET_CLIENT.event
def open_event(data):
    main.routes.open()


@SOCKET_CLIENT.event
def command_event(message):
    print("[Socket thread] : Comando recebido")
    config = main.methods.load_from_device_config()
    output = methods.run_command(message["data"])
    SOCKET_CLIENT.emit(
        "get_rasp_output",
        {
            "out": output,
            "room": config["code"],
        },
    )


@SOCKET_CLIENT.event
def connect_error():
    print("[Socket thread] : Falha na conexão")


@SOCKET_CLIENT.event
def disconnect():
    print("[Socket thread] : Desconectado pelo servidor")
