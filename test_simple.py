#!/usr/bin/env python3
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_simple_request():
    session = requests.Session()
    
    # Configure retries
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print("Testing connection to httpbin.org...")
        response = session.get(
            "http://httpbin.org/ip", 
            headers=headers,
            timeout=10,
            verify=False
        )
        print(f"Success! Status: {response.status_code}")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    test_simple_request()