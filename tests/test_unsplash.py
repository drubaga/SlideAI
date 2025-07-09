import requests
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
QUERY = "sunset"
TIMES = []

params = {"query": QUERY, "client_id": UNSPLASH_ACCESS_KEY, "per_page": 1}

for i in range(5):
    start = datetime.datetime.now()
    resp = requests.get("https://api.unsplash.com/search/photos", params=params)
    elapsed = (datetime.datetime.now() - start).total_seconds()
    TIMES.append(elapsed)
    print(f"[Unsplash] Request {i+1}: {elapsed:.3f}s — status {resp.status_code}")
    time.sleep(1)

avg = sum(TIMES) / len(TIMES)
print(f"\nUnsplash average response time: {avg:.3f}s")
