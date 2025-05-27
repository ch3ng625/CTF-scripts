from base64 import b64encode, b64decode
from random import shuffle
import string
import sys
import socket
import time
from colorama import Fore, Style

# Training message: This input is deliberately constructed to trigger every single character in the base64 alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/---additional-entropy-to-hit-edge-cases.

STANDARD_ENCODING    = list(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')
INTERCEPTED_ENCODING = {}

def learn_mapping(sock, msg):
    msg_b64 = b64encode(msg).strip(b'=')
    
    sock.sendall(b'1\n')
    time.sleep(1)
    sock.recv(1024)

    sock.sendall(msg + b'\n')
    time.sleep(1)
    resp = sock.recv(1024)
    transcoded = resp.split(b'\n')[0]

    for std_chr, int_chr in zip(msg_b64, transcoded):
        INTERCEPTED_ENCODING[chr(int_chr)] = chr(std_chr)
    
    print(Fore.YELLOW + f"[!] Character mapping {len(INTERCEPTED_ENCODING)}/64 completed." + Style.RESET_ALL)
    if (len(INTERCEPTED_ENCODING) == 64):
        print(Fore.GREEN + "[+] Character mapping completed." + Style.RESET_ALL)
    print()

def recover(sock):
    sock.sendall(b'2\n')
    time.sleep(1)
    resp = sock.recv(1024)

    flag_enc = resp.split(b'\n')[0]
    print(Fore.BLUE + f"[*] Transcripted flag: {flag_enc.decode()}" + Style.RESET_ALL)

    flag_b64 = b''
    for i in range(len(flag_enc)):
        if chr(flag_enc[i]) in INTERCEPTED_ENCODING:
            flag_b64 += INTERCEPTED_ENCODING[chr(flag_enc[i])].encode()
        else:
            flag_b64 += b'?'
    
    print(Fore.BLUE + f"[*] Base64-encoded flag: {flag_b64.decode()}" + Style.RESET_ALL)
    if b'?' not in flag_b64:
        padding = len(flag_b64.decode()) % 4
        if padding:
            flag_b64 += b'=' * (4 - padding)
        print(Fore.GREEN + f"[+] FLAG: {b64decode(flag_b64.decode()).decode()}" + Style.RESET_ALL)



def main():
    if len(sys.argv) != 3:
        print(Fore.RED + f"[-] Usage: {sys.argv[0]} <host> <port>" + Style.RESET_ALL)
        return
    
    host = sys.argv[1]
    port = int(sys.argv[2])

    # connection init
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.recv(1024)
    time.sleep(1)

    # build mapping
    print(Fore.BLUE + "[*] Building character mapping..." + Style.RESET_ALL)
    while len(INTERCEPTED_ENCODING) != 64:
        message = input(Fore.BLUE + "[*] Enter training message (enter 'exit' to abort) >> " + Style.RESET_ALL)
        if message == "exit":
            print(Fore.YELLOW + '[!] Character mapping aborted manually' + Style.RESET_ALL)
            print()
            break
        learn_mapping(s, message.encode())
    
    print(Fore.BLUE + "[*] Recovering flag..." + Style.RESET_ALL)
    recover(s)

    s.close()
    return

if __name__ == '__main__':
    main()