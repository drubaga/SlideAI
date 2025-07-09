import os
import requests
from serpapi import GoogleSearch
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import re

load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

class SerpApiImageGenerator:
    def __init__(self, image_dir="images"):
        self.image_dir = image_dir
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def fetch_image(self, keywords: str) -> str:
        try:
            query = " ".join(keywords) if isinstance(keywords, list) else keywords
            print(f"[INFO] Searching SerpAPI for: {query}")

            search = GoogleSearch({
                "q": query,
                "tbm": "isch",
                "num": 1,
                "api_key": SERPAPI_API_KEY
            })

            results = search.get_dict()
            images = results.get("images_results", [])

            if not images:
                print(f"[WARN] No images found for '{query}'")
                return None

            image_url = images[0].get("original") or images[0].get("thumbnail")
            if not image_url:
                print(f"[ERROR] No valid image URL found for '{query}'")
                return None

            # Fetch and validate image
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content))  # validate image
            safe_filename = re.sub(r"[^\w\-_. ]", "_", query)
            file_path = os.path.join(self.image_dir, f"{safe_filename}_serpapi.jpg")
            image.save(file_path)

            print(f"[INFO] Image saved for '{query}' → {file_path}")
            return file_path

        except Exception as e:
            print(f"[SERPAPI ERROR] {e}")
            return None
