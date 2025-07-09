import requests
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
QUERY = "sunset"
TIMES = []

params = {
    "engine": "google",
    "q": QUERY,
    "api_key": SERPAPI_KEY,
    "tbm": "isch",  # image search
    "ijn": "0"
}

for i in range(5):
    start = datetime.datetime.now()
    response = requests.get("https://serpapi.com/search", params=params)
    elapsed = (datetime.datetime.now() - start).total_seconds()
    TIMES.append(elapsed)
    print(f"[SerpApi] Request {i+1}: {elapsed:.3f}s — status {response.status_code}")
    time.sleep(1)

avg = sum(TIMES) / len(TIMES)
print(f"\n SerpApi average response time: {avg:.3f}s")
