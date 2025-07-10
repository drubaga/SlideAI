import os
import requests
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

class PexelsImageGenerator:
    """
    A utility class that uses the Pexels API to fetch an image based on a keyword query
    and saves it locally for use in presentations or other applications.
    """
    def __init__(self, image_dir="images"):
        """
        Initializes the image generator and ensures the output directory exists.

        Args:
            image_dir (str): Directory where the downloaded images will be saved.
        """
        self.image_dir = image_dir
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def fetch_image(self, keywords: str) -> str:
        """
        Searches the Pexels API for an image matching the given keywords and saves it locally.

        Args:
            keywords (str or list): Search query string or list of keyword strings.

        Returns:
            str: Path to the saved image file, or None if no image was found or an error occurred.
        """
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
