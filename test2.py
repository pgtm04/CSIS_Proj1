import socket
from flask import Flask, render_template, request
app = Flask(__name__)


s = socket.socket()
print ("Socket successfully created")

port = 54321

s.bind(('', port))
print ("socket binded to %s" %(port))

s.listen(5)
print ("socket is listening")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form.get("message")
        if message:
            s.settimeout(2.0)  # Times out after 2 seconds instead of waiting forever
            try:
                c, addr = s.accept()
                c.send(message.encode()+b'from server2')
                c.close()
            except socket.timeout:
                print("No client connected in time.")
            except Exception as e:
                print(f"Error: {e}")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True, use_reloader=False)