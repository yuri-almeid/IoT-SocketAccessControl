from app import SOCKETIO as socketio
from app import create_app

app = create_app()

if __name__ == "__main__":
    socketio.run(app, port=5001)
