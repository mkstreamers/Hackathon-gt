import whois
import requests
import socket
from datetime import datetime
from urllib.parse import urlparse

def check_ssl(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme == "https"

def check_domain_age(domain):
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age = (datetime.now() - creation_date).days
        return age
    except Exception as e:
        print(f"Error fetching domain age: {e}")
        return None

def check_blocklist(url):
    blocklisted_domains = ["example.com", "phishingsite.com"]
    domain = urlparse(url).netloc
    return domain in blocklisted_domains

def whois_lookup(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except Exception as e:
        print(f"Error fetching WHOIS data: {e}")
        return None

def is_genuine_website(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # Initialize genuineness score
    genuineness_score = 0
    max_score = 3

    # Check SSL
    if check_ssl(url):
        print("The website has SSL enabled (HTTPS).")
        genuineness_score += 1
    else:
        print("Warning: The website does not have SSL enabled (HTTPS).")
  
    # Check Domain Age
    age = check_domain_age(domain)
    if age:
        if age < 180:  # Less than 6 months old
            print("Warning: The website's domain is less than 6 months old.")
        else:
            print(f"The website's domain is {age} days old.")
            genuineness_score += 1
    else:
        print("Domain age could not be determined.")
    
    # Check Blocklist
    if check_blocklist(url):
        print("Warning: The website is listed in a blocklist.")
    else:
        print("The website is not listed in a blocklist.")
        genuineness_score += 1
    
    # WHOIS Lookup (Optional: could be used for more checks)
    domain_info = whois_lookup(domain)
    if domain_info:
        print("WHOIS Information:")
        print(domain_info)

    # Final decision based on genuineness score
    print("\nFinal Analysis:")
    if genuineness_score == max_score:
        print("The website appears to be genuine.")
    else:
        print("The website might be suspicious. Please proceed with caution.")

if __name__ == "__main__":
    url = input("Enter website URL: ")
    is_genuine_website(url)
