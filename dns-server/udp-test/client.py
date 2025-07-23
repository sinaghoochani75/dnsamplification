import socket

UDP_IP = "10.0.1.10"
UDP_PORT = 8543
MESSAGE = "Hi, can you listen to this?"

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE, 'ascii'), (UDP_IP, UDP_PORT))
