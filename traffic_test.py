import requests
import time

# generates repeated traffic
for i in range(20):

    response = requests.get(
        "http://127.0.0.1:8000/users"
    )
    print(response.json())
    time.sleep(1)