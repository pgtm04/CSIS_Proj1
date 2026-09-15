import socket
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=["*"])
room_histories = {}
sid_to_device = {}
sid_to_room = {}

@app.route('/')
def index():
    return render_template('index.html', message_history=message_history)


@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')

@app.route('/create-new.html')
def create_new():
    return render_template('create-new.html')


@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room', 'default')
    device_id = data.get('deviceId', 'Anonymous')

    # Track device info and join socket room
    sid_to_device[request.sid] = device_id
    sid_to_room[request.sid] = room
    join_room(room)

    # ADD TO CREATE NEW
    if room not in room_histories:
        room_histories[room] = []

    # Send existing room history to the connecting device
    emit('load_history', {'history': room_histories[room]})

@socketio.on('register_device')
def handle_register(data):
    device_id = data.get('deviceId', 'Anonymous')
    sid_to_device[request.sid] = device_id

@socketio.on('client_message')
def handle_client_message(data):
     msg = data.get('message')
     if msg:
         sender_name = sid_to_device.get(request.sid, "Anonymous")
         form_msg =f"{sender_name}: {msg}"
         message_history.append(form_msg)
         emit('server_response', {'message': form_msg}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
