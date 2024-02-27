import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('localhost', 12345)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)

# The socket is now listening for connections, but we're not accepting them
# The program will continue running, keeping the socket open in a listening state
while True:
    pass
