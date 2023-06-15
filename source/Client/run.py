import os
import threading
import time

from app import IS_EMBEDDED, SOCKET_CLIENT, create_app, main

app = create_app()


def socket_thread():
    config = main.methods.load_from_device_config()
    count = 0
    timestep = 5
    while True:
        try:
            SOCKET_CLIENT.connect(
                config["server_url"],
                wait=True,
                wait_timeout=30,
            )
            SOCKET_CLIENT.wait()
        except Exception as e:  # noqa
            print("[Socket thread] : Falha ao conectar ao servidor...")
            time.sleep(timestep)
            count += timestep
            if count >= 1800:
                if IS_EMBEDDED:
                    os.system("sudo reboot")


if __name__ == "__main__":

    socket_thread = threading.Thread(target=socket_thread)
    socket_thread.start()

    app.run(
        debug=False,
        host="127.0.0.1",
        port=5003,
        threaded=False,
        processes=2,
    )
