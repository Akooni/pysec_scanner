import subprocess
import socket

common_ports = [21,22,23,25,80,110,143,443,3389]


def is_host_up(ip):
    result = subprocess.run (
        ["ping","-c", "1", ip],
        stdout= subprocess.DEVNULL,
        stderr = subprocess.DEVNULL

    )
    if result.returncode == 0:
        return True
    else:
        return False
    


def scan_network(base_ip,start,end):
    for host in range (start,end + 1):
        ip = base_ip + str(host)
    
        if is_host_up(ip) == True:
            print(f"{ip} is UP")
            scan_ports_for_hosts(ip)

def is_port_open(ip,port):
    # 1. create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. set timeout
    s.settimeout(0.5)
    # 3. call connect_ex
    result = s.connect_ex((ip,port))
    # 4. close socket
    s.close()
    # 5. return True/False based on result
    if result == 0:
        return True
    else:
        return False
    


def scan_ports_for_hosts(ip):
    print(f"\nScanning common ports on {ip}")
    #1 loop through the common ports
    for port in common_ports:

        if is_port_open(ip,port):
            print(f"Port {port} is OPEN")
    #2 use the port in is port open

    
        




if __name__ == "__main__":
    pass