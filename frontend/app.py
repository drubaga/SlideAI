import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from local .env file
load_dotenv()

# Get backend URL from environment or fallback to localhost
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("SlideAI Frontend")

user_query = st.text_input("Enter your prompt")
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

# Template selection
template = st.selectbox("Choose Slide Template", ["default", "company"])

# Image settings
enable_images = st.checkbox("Include Images", value=True)
image_provider = None
if enable_images:
    image_provider = st.selectbox("Choose Image Provider", ["pexels", "serpapi"])

if st.button("Generate Slides") and uploaded_file is not None and user_query:
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    payload = {
        "user_query": user_query,
        "text_path": file_path,
        "enable_images": enable_images,
        "image_provider": image_provider,
        "template": template
    }

    try:
        response = requests.post(f"{BASE_URL}/generate-pptx", json=payload)

        if response.status_code == 200:
            st.success(" Presentation generated!")
            st.download_button(
                label="Download PPTX",
                data=response.content,
                file_name="slides.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        else:
            st.error(f" Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f" Failed to connect to backend: {e}")
