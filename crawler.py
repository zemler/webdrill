import requests
import argparse
from urllib.parse import urljoin

def main():
    parser = argparse.ArgumentParser(description="Default Arguments")
    parser.add_argument('-t', '--target', required=True, help="Target domain or IPv4 address")
    parser.add_argument('-m', '--method', choices=['GET', 'HEAD', 'POST'], default='GET', help="HTTP Method")
    parser.add_argument('-w', '--wordlist', required=True, help="Path to wordlist")
    parser.add_argument('--status-code', type=int, default=200, help="Response status code filter")
    
    args = parser.parse_args()
    method = args.method.upper()
    
    try:
        with open(args.wordlist, 'r') as wordlist:
            words = wordlist.read().splitlines()  
    except FileNotFoundError:
        print(f"[-] Unable to find wordlist: {args.wordlist}")
        return
    except Exception as e:
        print(f"[-] Error Occurred: {e}")
        return
    
    for line in words:
        url = urljoin(args.target, line)  
        
        try:
            if method == 'GET':
                r = requests.get(url)
            elif method == 'HEAD':
                r = requests.head(url)
            elif method == 'POST':
                r = requests.post(url)
            else:
                print(f"[!] Unrecognized method: {method}, using default GET!")
                r = requests.get(url) 
            
            if r.status_code == args.status_code:
                print(f"[+] Found: {url} Status code: {r.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"[-] Error in URL {url}: {e}")
            
if __name__ == "__main__":
    main()
