import socket
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
message_history = []
port = 54321
@app.route('/', methods=['GET'])
def home():
    try:
        s = socket.socket()
        s.connect(('127.0.0.1', port))

        data_from = s.recv(1024)
        res = data_from.decode()
        s.close()
    except Exception as e:
        res = f"Could not connect to server: {e}"
    message_history.append(res)
    return render_template('index.html', message_history=message_history)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
