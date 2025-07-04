# Use official Python slim image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Now copy the full source code into the container
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
