import socket
import threading
from flask import Flask, render_template, request
app = Flask(__name__)
pending_messages = []

def run_socket_server():
    port = 54321
    s = socket.socket()
    print ("Socket successfully created")
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    print ("socket binded to %s" %(port))
    s.listen(5)
    print ("socket is listening")

    while True:
        try:
            c, addr = s.accept()
            message = pending_messages.pop(0) if pending_messages else ""
            c.send(message.encode())
            c.close()
        except Exception as e:
            print(f"Socket Error: {e}")

threading.Thread(target=run_socket_server, daemon=True).start()
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form.get("message")
        if message:
            pending_messages.append(message)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True, use_reloader=False)