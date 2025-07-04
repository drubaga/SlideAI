# SlideAI 

SlideAI is a FastAPI-based backend service that generates AI-powered slide content from raw `.txt` files using OpenAI's large language models (LLMs). It transforms user queries and supporting source material into structured slide-ready content—ideal for automating presentation workflows.

---

## Features:

-  REST API built with FastAPI
-  LLM integration via OpenAI API (e.g., GPT-4o)
-  Reads raw `.txt` files as input context
-  Structured JSON output for slide content
-  Retry logic for resilient API calls using `tenacity`
-  Secure configuration with `.env`

---

##  Project Structure

```text
SlideAI/
├── app/
│   └── main.py                 # FastAPI application entry point
├── src/
│   ├── llm.py                  # LLM client wrapper with retry and kwargs support
│   ├── config.py               # Loads OpenAI config from environment
│   └── prompts/
│       ├── prompt_manager.py   # Builds structured system prompts
│       └── prompt_templates.py # Raw prompt templates
├── data/                       # Input .txt files
├── tests/                      # (Optional) test suite
├── .env                        # API key and config values
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
```

## Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

**Key Packages:**

- **fastapi** – REST API framework  
- **openai** – OpenAI Python SDK  
- **pydantic** – Data validation  
- **tenacity** – Retry strategy  
- **python-dotenv** – Load config from `.env`  
- **uvicorn** – ASGI server  
- **python-pptx** – *(Optional)* for future slide generation  

## Environment Setup

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
