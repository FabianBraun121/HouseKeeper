import socket

ip = socket.gethostbyname(socket.gethostname())
gate = 6969
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((ip, gate))

while True:
    data, sensor_address = server_socket.recvfrom(1024)
    # Process the received data and take appropriate actions
    print(f"Received data from {sensor_address}: {data}")