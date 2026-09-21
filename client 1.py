import socket
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=["*"])
room_histories = {"default": []}
sid_to_device = {}
sid_to_room = {}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')

@app.route('/create-new.html')
def create_new():
    return render_template('create-new.html')


@socketio.on('join_room')
def handle_join_room(data):
    device_id = data.get('deviceId', 'Anonymous')
    room = data.get('room', 'default')
    if room in room_histories:
        sid_to_device[request.sid] = device_id
        sid_to_room[request.sid] = room
        join_room(room)
        print(room)
        emit('load_history', {'success': True, 'room': room, 'history': room_histories[room]}, to=request.sid)
    else:
        emit('load_history', {'success': False}, to=request.sid)

@socketio.on('register_device')
def handle_register(data):
    device_id = data.get('deviceId', 'Anonymous')
    sid_to_device[request.sid] = device_id

@socketio.on('client_message')
def handle_client_message(data):
     msg = data.get('message')
     room = sid_to_room.get(request.sid, 'default')
     if msg:
         sender_name = sid_to_device.get(request.sid, "Anonymous")
         formatted_msg = f"{sender_name}: {msg}"

         if room not in room_histories:
             room_histories[room] = []

         room_histories[room].append(formatted_msg)
         join_room(room)
         emit('server_response', {'message': formatted_msg}, to=room)


@socketio.on('create_room')
def handle_create_room(data):
    room_name = data.get('room_name')
    if room_name and room_name not in room_histories:
        room_histories[room_name] = []
        emit('room_created', {'room': room_name, 'success': True})
    else:
        emit('room_created', {'room': room_name, 'success': False, 'message': 'Room already exists!'})

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
