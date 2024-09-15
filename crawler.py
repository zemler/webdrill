import requests
import argparse
from urllib.parse import urljoin
import warnings
from urllib3.exceptions import InsecureRequestWarning

def main():
    parser = argparse.ArgumentParser(description="Web crawler with customizable options")
    parser.add_argument('-t', '--target', required=True, help="Target domain or IPv4 address")
    parser.add_argument('-m', '--method', choices=['GET', 'HEAD', 'POST'], default='GET', help="HTTP Method")
    parser.add_argument('-w', '--wordlist', required=True, help="Path to wordlist")
    parser.add_argument('--status-code', type=int, default=200, help="Response status code filter")
    parser.add_argument('-o', '--output-file', help="Path to output file")
    parser.add_argument('--ignore-cert', action='store_true', help="Ignore SSL certificate warnings")
    parser.add_argument('--cookie', help="Session cookie in the format 'name=value'. Example: PHPSESSID=qwertyuiop123456")
    
    args = parser.parse_args()
    method = args.method.upper()
    verify_ssl = not args.ignore_cert
    warnings.simplefilter('ignore', InsecureRequestWarning)
    findings = []
    headers = {}
    if args.cookie:
        headers['Cookie'] = args.cookie
    
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
                r = requests.get(url, verify=verify_ssl, headers=headers)
            elif method == 'HEAD':
                r = requests.head(url, verify=verify_ssl, headers=headers)
            elif method == 'POST':
                r = requests.post(url, verify=verify_ssl, headers=headers)
            else:
                print(f"[!] Unrecognized method: {method}, using default GET!")
                r = requests.get(url, verify=verify_ssl, headers=headers)
            
            if r.status_code == args.status_code:
                print(f"[+] Found: {url} Status code: {r.status_code}")
                finding = f"[+] Found: {url} Status code: {r.status_code}\n"
                findings.append(finding)
        
        except requests.exceptions.RequestException as e:
            print(f"[-] Error in URL {url}: {e}")
    
    if args.output_file:
        try:
            with open(args.output_file, 'w') as file:
                for line in findings:
                    file.write(line)
            print(f"[+] Findings saved to {args.output_file}")
        except Exception as e:
            print(f"[-] Error while creating file: {e}")

if __name__ == "__main__":
    main()
