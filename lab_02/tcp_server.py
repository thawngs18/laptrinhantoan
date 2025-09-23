import socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_ip = "127.0.0.1"
server_port = 8080
server_socket.bind((server_ip,server_port))
server_socket.listen(1)
print(f"Server dang lang nghe tai {server_ip}:{server_port}")
conn, addr = server_socket.accept()
print(f"Ket noi tu {addr}")
conn.send(b"Hello,Client!")
data = conn.recv(1024)
print(f"Da nhan: {data.decode()}")
conn.close()
server_socket.close()