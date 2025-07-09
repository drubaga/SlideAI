import os
import requests
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

class PexelsImageGenerator:
    
    def __init__(self, image_dir="images"):
        self.image_dir = image_dir
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def fetch_image(self, keywords: str) -> str:
        # Ensure keywords is a string
        if isinstance(keywords, list):
            keywords = " ".join(keywords)
            
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": keywords, "per_page": 1}
        try:
            response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
            response.raise_for_status()
            results = response.json()
            url = results["photos"][0]["src"]["original"]
            image_path = os.path.join(self.image_dir, f"{keywords.replace(' ', '_')}_pexels.jpg")
            img_data = requests.get(url).content
            with open(image_path, "wb") as f:
                f.write(img_data)
            return image_path
        except Exception as e:
            print(f"[PEXELS ERROR] {e}")
            return None
