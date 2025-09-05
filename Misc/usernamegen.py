import sys
import os
from colorama import Fore, Style

def help():
    print(f"Usage: {sys.argv[0]} <namelist.txt> <output.txt> [<domain>]")
    exit(0)

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

def main():
    if len(sys.argv) not in [3,4]:
        help()
    namelist = sys.argv[1]
    output = sys.argv[2]
    domain = ""
    if len(sys.argv) == 4:
        domain = sys.argv[3]
    
    if not os.path.exists(namelist):
        log("error", f"{namelist} not found.")
        exit(0)
    
    if os.path.exists(output):
        log("error", f"{output} already exists, choose another name.")
        exit(0)
    
    with open(namelist, 'r') as f:
        names = [line.strip() for line in f if line.strip()]
    
    usernames = set()
    for n in names:
        fname = n.split()[0]
        lname = n.split()[1]

        # JohnDoe, John.Doe, John-Doe, John_Doe
        usernames.add(f"{fname}{lname}")
        usernames.add(f"{fname}.{lname}")
        usernames.add(f"{fname}-{lname}")
        usernames.add(f"{fname}_{lname}")

        # DoeJohn, Doe.John, Doe-John, Doe_John
        usernames.add(f"{lname}{fname}")
        usernames.add(f"{lname}.{fname}")
        usernames.add(f"{lname}-{fname}")
        usernames.add(f"{lname}_{fname}")

        # JohnD, John.D, John-D, John_D
        usernames.add(f"{fname}{lname[0]}")
        usernames.add(f"{fname}.{lname[0]}")
        usernames.add(f"{fname}-{lname[0]}")
        usernames.add(f"{fname}_{lname[0]}")

        # DJohn, D.John, D-John, D_John
        usernames.add(f"{lname[0]}{fname}")
        usernames.add(f"{lname[0]}.{fname}")
        usernames.add(f"{lname[0]}-{fname}")
        usernames.add(f"{lname[0]}_{fname}")

        # JDoe, J.Doe, J-Doe, J_Doe
        usernames.add(f"{fname[0]}{lname}")
        usernames.add(f"{fname[0]}.{lname}")
        usernames.add(f"{fname[0]}-{lname}")
        usernames.add(f"{fname[0]}_{lname}")

        # DoeJ, Doe.J, Doe-J, Doe_J
        usernames.add(f"{lname}{fname[0]}")
        usernames.add(f"{lname}.{fname[0]}")
        usernames.add(f"{lname}-{fname[0]}")
        usernames.add(f"{lname}_{fname[0]}")

        usernames.add(fname)
        usernames.add(lname)
    
    with open(output, 'w') as f:
        for u in usernames:
            f.write(f"{u}\n")
            if domain != "":
                f.write(f"{u}@{domain}\n")
    
    log("success", f"Done. Output saved in {output}.")
    return

if __name__ == "__main__":
    main()