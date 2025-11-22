#!/usr/bin/env python3
import subprocess
import socket


#Variables that needed to make the rest work
common_ports = [21,22,23,25,80,110,143,443,3389]
service_names = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3389: "RDP"
}

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"


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
            print("\n" + "-" * 50)
            print(f"{GREEN}Host: {ip}  ✓ ONLINE{RESET}")
            print("-" * 50)

            open_ports = scan_ports_for_hosts(ip)
            
            ssh_banner(ip)
            port_vulnerabilities(ip,open_ports)
            print("-" * 50)

            
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
    print(f"Open Ports:")
    #1 loop through the common ports
    port_none = False
    open_ports = []
    for port in common_ports:
        #2 use the port in is_port_open function
        if is_port_open(ip,port):
            port_none= True
            print(f"   • {port} ({service_names[port]})")
            open_ports.append(port)
    if not port_none:
        print(f"• {CYAN}None{RESET}")
        #3 if not True print the port is closed
    return open_ports


#take an ip
#check it's open ports
#print warining based on the rules

def port_vulnerabilities(ip,open_ports):
    print(f"\nVulnerabilities:\n")
    #used this method so if no ports were open it show None
    found_vulnerability = False


    if 21 in open_ports:    
        print(f"{RED}⚠ FTP detected — sends passwords in plaintext (insecure){RESET}")
        found_vulnerability = True
        
    if 22 in open_ports:
        print(f"{YELLOW}⚠ SSH detected — could lead to Unauthorized Access & System Compromise{RESET}")
        banner = ssh_banner(ip)
        if banner:
            print(f"SSH Banner: {banner.strip()}")
            found_vulnerability = True

            if "OpenSSH_5" in banner or "OpenSSH_6" in banner:
                print("⚠ Outdated SSH version — vulnerable to multiple known CVEs")
                found_vulnerability = True
                
            if "OpenSSH_3" in banner or "OpenSSH_4" in banner:
                print("⚠ CRITICAL: Very old SSH version detected — extremely insecure")
                found_vulnerability = True

            if "dropbear" in banner.lower():
                print(" Dropbear is detected — common on Iot devices, might be weakly configured")
                found_vulnerability = True
        else:
            print("SSH is detected, but banner could not be retrieved")
            found_vulnerability = True
        


    if 23 in open_ports:
        print(f"{RED}⚠ Telnet detected — no encryption,highly insecure{RESET}")
        found_vulnerability = True

    if 80 in open_ports and 443 not in open_ports:
        print(f"{RED}⚠ HTTP without HTTPS — traffic is not encrypted{RESET}")
        found_vulnerability = True

    if 3389 in open_ports:
        print(f"{RED}⚠ RDP detected — remote desktop exposed, consider restricting access{RESET}")
        found_vulnerability = True

    if not found_vulnerability:
        print(f"{CYAN}• No obvious vulnerabilities detected{RESET}")






def ssh_banner(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    result = s.connect_ex((ip,22))
    if result != 0:
        s.close()
        return None
    
    data = s.recv(1024)
    banner = data.decode(errors="ignore")
    s.close()
    return banner

    


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