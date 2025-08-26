#!/usr/bin/env python3

import requests
import time

def test_connection():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "Accept-Encoding": "none",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
    }
    
    url = "https://hianime.nz"
    
    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}: Testing connection to {url}")
            response = requests.get(
                url, 
                headers=headers, 
                timeout=10,
                verify=True
            )
            response.raise_for_status()
            print(f"Success! Status: {response.status_code}")
            print(f"Content length: {len(response.content)}")
            return response
            
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {e}")
        except requests.exceptions.SSLError as e:
            print(f"SSL error: {e}")
        except Exception as e:
            print(f"Other error: {e}")
            
        if attempt < 2:
            wait_time = 5
            print(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
    
    print("All attempts failed!")
    return None

if __name__ == "__main__":
    test_connection()