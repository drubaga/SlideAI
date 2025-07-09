import requests
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
QUERY = "sunset"
TIMES = []

headers = {"Authorization": PEXELS_API_KEY}
params = {"query": QUERY, "per_page": 1}

for i in range(5):
    start = datetime.datetime.now()
    resp = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    elapsed = (datetime.datetime.now() - start).total_seconds()
    TIMES.append(elapsed)
    print(f"[Pexels] Request {i+1}: {elapsed:.3f}s — status {resp.status_code}")
    time.sleep(1)

avg = sum(TIMES) / len(TIMES)
print(f"\n Pexels average response time: {avg:.3f}s")
