import socket
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')
message_history = []
port = 54321
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', message_history=message_history)

def read_tcp_stream():
    s = socket.socket()
    try:
        s.connect(('127.0.0.1', port))
    except Exception as e:
        print(f"Could not connect to backend server: {e}")
        return
    while True:
        try:
            data_from = s.recv(1024)
            if not data_from:
                break
            res = data_from.decode().strip()
            if res and res not in message_history:
                message_history.append(res)
                # Pushes the message to the UI instantly
                socketio.emit('new_message', {'message': res})
        except Exception as e:
            print(f"Error reading socket: {e}")
            break

@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(read_tcp_stream)


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True, allow_unsafe_werkzeug=True)
