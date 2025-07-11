# SlideAI 

SlideAI is a full-stack AI-powered slide generator. It includes a FastAPI backend service that generates structured presentation content from .txt files using OpenAI’s LLMs, and a Streamlit-based frontend that allows users to interactively upload files, input queries, and download .pptx slides.

---

## Features:

- REST API built with FastAPI
- Streamlit web frontend for file upload and download
- LLM integration via OpenAI API (GPT-4o)
- Reads raw `.txt` files as input context
- Structured JSON output for slide content
- Retry logic for resilient API calls using `tenacity`
- Secure configuration with `.env`
- Dynamic image generation with support for:
  - No images
  - Pexels API
  - SerpAPI (Google Images)
- PowerPoint template support:
  - Default and custom templates (e.g., company-branded)
  - Preserves original layout, fonts, and styling


---

##  Project Structure

```text
SlideAI/
├── app/
│   └── main.py                 # FastAPI backend entry point
├── frontend/
│   └── app.py                  # Streamlit frontend application
├── src/
│   ├── llm.py                  # LLM client wrapper
│   ├── config.py               # Loads OpenAI config from env
│   ├── models/
│   │   └── presentation.py   
│   ├── prompts/
│   │   ├── prompt_manager.py   # Prompt logic
│   │   └── prompt_templates.py # Prompt templates
│   ├── image_generators/
│   │   ├── pexels_image_generator.py
│   │   └── serpapi_image_generator.py
│   └── pptx_generator/
│       └── builder.py          # PPTX generation logic
├── data/                       # Input .txt files
├── output/                     # Generated .pptx files
├── images/                     # Downloaded image assets
├── templates/                  # PowerPoint templates
├── .env                        # API credentials
├── .gitignore
├── dockerfile
├── makefile
├── requirements.txt
└── README.md
```


---

## Environment Variables

Make sure to create a `.env` file in the root directory with the following:

```env
OPENAI_API_KEY=your-openai-api-key-here
BACKEND_URL=your-backend-url
SERPAPI_API_KEY=your_real_key_here
PEXELS_API_KEY=your_pexels_api_key_here
```

## Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

**Key Packages:**

- **fastapi** – REST API framework  
- **openai** – OpenAI Python SDK 
- **streamlit** – Frontend UI 
- **pydantic** – Data validation  
- **tenacity** – Retry strategy  
- **python-dotenv** – Load config from `.env`  
- **uvicorn** – ASGI server  
- **python-pptx** – *(Optional)* for future slide generation  
- **google-search-results** – SerpAPI Python SDK for Google Images integration


## Backend Setup

### 1. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```
### 2. Activate the Virtual Environment

**On macOS/Linux:**

```bash
source venv/bin/activate
```

**On Windows:**

```bash
venv\Scripts\activate
```

### 3. Running the Application
Run the FastAPI app with Uvicorn:

```bash
uvicorn app.main:app --reload
```

Then open your browser to:
- http://127.0.0.1:8000/health – Health check
- http://127.0.0.1:8000/docs – Interactive Swagger docs

## Frontend (Streamlit)

### 1. Navigate to frontend/ and run the app:

```bash
cd frontend
streamlit run app.py
```
### 1. What it does:
- Lets users upload .txt files
- Prompts user for query
- Calls the backend API
- Allows downloading of the generated .pptx file


## Docker Usage

You can run the SlideAI backend inside a Docker container for isolated, reproducible deployments.

### 1. Build the Docker Image

```bash
docker build -t slideai-backend .
```
### 2. Run the Container

Make sure you have a .env file in the project root with your OpenAI API key, and that your input .txt files are stored in the data/ directory.

```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  --name slideai-container \
  slideai-backend
```

- `--env-file .env` loads your OpenAI credentials into the container.

- `-v $(pwd)/data:/app/data` mounts your local `data/` folder into the container so your `.txt` input files can be accessed by the app.

### 3. Access the App

- **Health check:** [http://localhost:8000/health](http://localhost:8000/health)  
- **Interactive docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
