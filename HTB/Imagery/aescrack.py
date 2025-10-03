import os
import pyAesCrypt

encrypted_file = "web_20250806_120723.zip.aes"
wordlist = "/usr/share/wordlists/rockyou.txt"

with open(wordlist, 'r', encoding='utf-8', errors='ignore') as file:
    passwords = file.readlines()

print(f"Trying {len(passwords)} passwords.")

counter = 0
valid = ""
for password in passwords:
    counter += 1
    print(f"[{counter}/{len(passwords)}] Trying {password.strip()} - ", end="")
    try:
        pyAesCrypt.decryptFile(encrypted_file, "decrypted.zip", password.strip())
    except:
        print("Fail                     ", end="\r")
        continue
    
    if (os.path.exists("decrypted.zip")):
        print("SUCCESS!")
        valid = password.strip()
        break

print(f"Password cracked: {valid}. Decypted file saved as decypted.zip.")