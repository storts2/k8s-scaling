import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8080/work"

CONCURRENT_USERS = 10

def send_request():
    try:
        response = requests.get(URL, timeout=30)
        return response.status_code
    except requests.RequestException:
        return None

print("Starting continuous workload...")

with ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:

    while True:
        futures = [
            executor.submit(send_request)
            for _ in range(CONCURRENT_USERS)
        ]
        
        for future in futures:
            future.result()

        time.sleep(0.1)