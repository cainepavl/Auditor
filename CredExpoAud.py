import requests
import hashlib
import sys
import os
import getpass
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform terminal support (Windows/Linux/macOS)
colorama.init()

def clear_screen():
    """
    Clears the terminal buffer to mitigate visual data exposure (shoulder surfing).
    """
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
def request_api_data(query_char):
    """
    Implements k-Anonymity by querying the HIBP 'Range' API.
    Only the first 5 characters of the SHA-1 hash are transmitted, 
    ensuring the full hash/password never leaves the local environment.
    """
    url = f'https://api.pwnedpasswords.com/range/{query_char}'
    res = requests.get(url, timeout=10)
    if res.status_code != 200:
       raise RuntimeError(f'API Connection Error: {res.status_code}. Verify network connectivity.')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    """
    Parses the API response to find a matching suffix and returns the leak frequency.
    """
    # Using a generator expression for memory-efficient string parsing
    hashes = (line.split(':', 1) for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    """
    Performs SHA-1 hashing and prepares the prefix/suffix for the k-Anonymity check.
    """
    # Convert password to SHA-1 hash
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # Split hash into first 5 chars (prefix) and the rest (tail)
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main():
    """
    Main execution loop. Uses getpass to prevent sensitive credentials 
    from being stored in shell history or process logs.
    """
    clear_screen()
    print(f"{Fore.CYAN}======================================")
    print(f"   CREDENTIAL EXPOSURE AUDITOR")
    print(f"======================================{Style.RESET_ALL}\n")
    
    # Securely prompt for input so characters aren't echoed to the screen
    # This prevents the password from appearing in 'bash_history' or 'cmd history'
    user_input = getpass.getpass("Enter password to audit (input hidden): ")
    
    if not user_input:
        print(f"\n{Fore.YELLOW}[!] No input detected. Operation aborted.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.WHITE}Auditing against known data breaches...{Style.RESET_ALL}")
    count = pwned_api_check(user_input)
    
    if count:
        print(f'\n{Fore.RED}[!] SECURITY ALERT: This password was found {count} times.')
        print(f'Recommendation: This credential is compromised. Rotate immediately.{Style.RESET_ALL}')
    else:
        print(f'\n{Fore.GREEN}[+] AUDIT PASSED: This password was not found in public datasets.{Style.RESET_ALL}')
    
    print(f"\n{Fore.CYAN}Audit Complete.{Style.RESET_ALL}")
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C to avoid messy traceback
        print(f"\n{Fore.YELLOW}\n[!] Audit cancelled by user.{Style.RESET_ALL}")
        sys.exit(0)
