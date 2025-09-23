import socket

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_ip = "127.0.0.1"   # trỏ tới server local
server_port = 8080   

try:
    client_socket.connect((server_ip,server_port))
    print(f"Da ket noi toi {server_ip} tai cong {server_port}")
    client_socket.send(b"Hello,Server!")
    response = client_socket.recv(1024)
    print(f"Phan hoi tu server: {response.decode()}")
except socket.error as e:
    print(f"Loi ket noi: {e}")
finally:
    client_socket.close()
