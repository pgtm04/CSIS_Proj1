import socket

port = 12345
s = socket.socket()
s.connect(('127.0.0.1', port))

while True:
    data_from = s.recv(1024)

    # Exit loop if connection is closed
    if not data_from:
        print("Server disconnected.")
        break

    print("Received data:", data_from.decode())

s.close()