import socket
import time
import threading
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

message_history = []
port = 54321
def poll_server():
    try:
        s = socket.socket()
        s.connect(('127.0.0.1', port))
        data_from = s.recv(1024)
        res = data_from.decode()
        s.close()
        if res:
            message_history.append(res)
    except Exception as e:
        pass
    time.sleep(1)

threading.Thread(target=poll_server, daemon=True).start()
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', message_history=message_history)

@app.route('/get-messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': message_history})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
