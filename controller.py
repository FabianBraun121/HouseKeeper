import socket
from constants import CENTRAL_IP, CENTRAL_GATE

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((CENTRAL_IP, CENTRAL_GATE))

while True:
    data, sensor_address = server_socket.recvfrom(1024)
    # Process the received data and take appropriate actions
    print(f"Received data from {sensor_address}: {data}")