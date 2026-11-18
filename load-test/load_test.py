import requests
import time
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

URL = "http://localhost:8080/work"

TOTAL_REQUESTS = 100
CONCURRENT_USERS = 10

def send_request(request_number):
    try:
        start = time.time()

        response = requests.get(URL, timeout=30)

        duration = time.time() - start
        
        if response.status_code == 200:

            data = response.json()

            hostname = data["hostname"]

            return {
                "request": request_number,
                "hostname": hostname,
                "duration": round(duration, 3),
                "status": "success"
            }
        
        return {
            "request": request_number,
            "status": "failed"
        }

    except requests.RequestException as error:
        return {
            "request": request_number,
            "status": "error",
            "message": str(error)
        }

print("Starting Kubernetes Load Test")

print("Total Requests:", TOTAL_REQUESTS)
print("Concurrent Users:", CONCURRENT_USERS)

start_time = time.time()

with ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:
    results = list(
        executor.map(send_request, range(1, TOTAL_REQUESTS + 1))
    )

end_time = time.time()

successful = [
    result for result in results
    if result.get("status") == "success"
]

failed = TOTAL_REQUESTS - len(successful)

print("\nLoad Test Results")

print("Total Requests:", TOTAL_REQUESTS)
print("Successful Requests:", len(successful))
print("Failed Requests:", failed)

print("Total Time:", round(end_time - start_time, 2), "seconds")
if successful:
    print("\nRequests Handled by Each Pod:")

    distribution = Counter(
        result["hostname"] for result in successful
    )
    
    for hostname, count in distribution.items():
        print(hostname, ":", count)

    average_time = sum(
        result["duration"] for result in successful
    ) / len(successful)

    print("\nAverage Response Time:", round(average_time, 3), "seconds")