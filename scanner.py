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
    pass


if __name__ == "__main__":
    pass