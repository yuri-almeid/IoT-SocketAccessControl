import time

from socketIO_client_nexus import LoggingNamespace, SocketIO


def on_pong_event(*args):
    end = time.time()
    print("on_pong_event", args)
    print("Round trip time:", end - start)


with SocketIO("localhost", 5000, LoggingNamespace) as socketIO:
    start = time.time()
    socketIO.emit("ping_event", {"data": "Ping sent!"})
    socketIO.on("pong_event", on_pong_event)
    socketIO.wait(seconds=1)
