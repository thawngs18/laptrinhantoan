import socket
def port_scanner(target,ports):
    print(f"Dang quet {target} .... ")
    for port in ports:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            socket.setdefaulttimeout(1)
            result = s.connect_ex((target,port))
            if result == 0:
                print(f"Cong {port} dang mo")
            else:
                print(f"Cong {port} dang dong")
target_ip = "127.0.0.1"
port_to_scan = [22,80,443,8080]
port_scanner(target_ip,port_to_scan)