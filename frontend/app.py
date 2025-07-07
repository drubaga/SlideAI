import streamlit as st
import requests
import os

st.title("SlideAI Frontend")

user_query = st.text_input("Enter your prompt")
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if st.button("Generate Slides") and uploaded_file is not None and user_query:
    # Save uploaded .txt to ./data/
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Prepare backend payload
    payload = {
        "user_query": user_query,
        "text_path": file_path
    }

    # Call backend to generate PPTX
    response = requests.post("http://localhost:8000/generate-pptx", json=payload)

    if response.status_code == 200:
        st.success("Presentation generated!")

        # Let the user download the presentation directly
        st.download_button(
            label="Download PPTX",
            data=response.content,
            file_name="slides.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
