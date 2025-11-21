import subprocess
import socket

common_ports = [21,22,23,25,80,110,143,443,3389]

# This send a ping command 1 packet per ip 
#if return code equals to 0 then ip is up
#else ip is down
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
    

#This loop through usr hosts
#then it combine the base ip with hosts in range
#after looping with ip and hosts it will use that ip 
#and call for is_host_up function if true print the ip is up
#in the end it calls for scan_ports_for_hosts and use ip as a parameter
def scan_network(base_ip,start,end):
    for host in range (start,end + 1):
        ip = base_ip + str(host)
    
        if is_host_up(ip):
            print(f"{ip} is UP")

            open_ports = scan_ports_for_hosts(ip)

            port_vulnerabilities(ip,open_ports)

        else:
            print(f"{ip} is DOWN")

            
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
    open_ports = []
    for port in common_ports:
        #2 use the port in is_port_open function
        if is_port_open(ip,port):
            print(f"Port {port} is OPEN")
            open_ports.append(port)

            print(open_ports)
        #3 if not True print the port is closed
        else:
            print(f"Port {port} is CLOSED")
    return open_ports


#take an ip
#check it's open ports
#print warining based on the rules

def port_vulnerabilities(ip,open_ports):
    print(f"Checking vulnerabilities for {ip}")

    if 21 in open_ports:    
        print("FTP detected — sends passwords in plaintext (insecure)")
        
    if 23 in open_ports:
        print("Telnet detected — no encryption,highly insecure")
        
    if 80 in open_ports and 443 not in open_ports:
        print("HTTP without HTTPS — traffic is not encrypted")

    if 3389 in open_ports:
        print("RDP detected — remote desktop exposed, consider restricting access")


#Taking user input and using it in scan_network function
if __name__ == "__main__":
    base_ip = input("Enter ip address e.g(192.168.1.): ")
    start = int(input("Enter First Host: "))
    end = int(input("Enter end Host: "))

    scan_network(base_ip,start,end)    


#ok so the next feature i want to when there is and open port it shows that could be 
# a vulrabinty 
#ex 23 port is u
# # ftp -> is open which is considered a vurnabitly
#  
# 
# for each different port it will show a different message so i will start with a one first 