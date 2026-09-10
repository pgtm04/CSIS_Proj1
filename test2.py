import socket, requests
from flask import Flask, render_template, request
app = Flask(__name__)


s = socket.socket()
print ("Socket successfully created")

port = 54321

s.bind(('', port))
print ("socket binded to %s" %(port))

s.listen(5)
print ("socket is listening")
c, addr = s.accept()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form.get("message")
        if message:
            c.send(message.encode()+b'from server2')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True, use_reloader=False)