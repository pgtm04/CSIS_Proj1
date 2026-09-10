import socket
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")
message_history = []

user_map = {}
user_counter = 0

@app.route('/')
def home():
    return render_template('index.html', message_history=message_history)

@socketio.on('connect')
def handle_connect():
    global user_counter
    if request.sid not in user_map:
        user_counter += 1
        user_map[request.sid] = f"User {user_counter}"

@socketio.on('client_message')
def handle_client_message(data):
     msg = data.get('message')
     if msg:
         sender_name = user_map.get(request.sid, "Anonymous")
         form_msg =f"{sender_name}: {msg}"
         message_history.append(form_msg)
         emit('server_response', {'message': form_msg}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
