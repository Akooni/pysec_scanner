import subprocess
import socket

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






if __name__ == "__main__":
    pass