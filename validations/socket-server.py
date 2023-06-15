from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on("ping_event")
def handle_ping_event(message):
    print("received ping: " + message["data"])
    emit("pong_event", {"data": "Pong received!"})


if __name__ == "__main__":
    socketio.run(app, host="localhost", port=5000)
