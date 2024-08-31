import whois
import requests
import socket
from datetime import datetime
from urllib.parse import urlparse

def check_ssl(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme == "https":
        return True
    else:
        return False

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
    if domain in blocklisted_domains:
        return True
    return False

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

  
    if not check_ssl(url):
        print("Warning: The website does not have SSL enabled (HTTPS).")
  
    age = check_domain_age(domain)
    if age and age < 180:  
        print("Warning: The website's domain is less than 6 months old.")
    
   
    if check_blocklist(url):
        print("Warning: The website is listed in a blocklist.")
    
    domain_info = whois_lookup(domain)
    if domain_info:
        print("WHOIS Information:")
        print(domain_info)


if _name_ == "_main_":
    url = input("Enter website URL: ")
    is_genuine_website(url)