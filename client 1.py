import os
import socket
from flask import Flask, render_template, request, url_for, send_from_directory
from flask_socketio import SocketIO, emit, join_room
from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=["*"])
room_histories = {"default": []}
sid_to_device = {}
sid_to_room = {}
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

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

@socketio.on('upload-file')
def handle_upload_file(data):
    room = sid_to_room.get(request.sid, 'default')
    if room not in room_histories:
        room_histories[room] = []
    file_bytes = data.get('file')
    original_name = data.get('name', 'uploaded_file')
    filename = secure_filename(original_name)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(filepath, 'wb') as f:
        f.write(file_bytes)

    join_room(room)
    formatted_msg = f"{sid_to_device.get(request.sid, "Anonymous")}: {(url_for('download_file', name=filename))}"
    room_histories[room].append(formatted_msg)

    emit('server_response', {'message':formatted_msg}, to=room)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
