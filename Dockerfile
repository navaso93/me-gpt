# Use Python 3.12.9 as the base image environment
FROM python:3.12.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency list into /app
COPY requirements.txt .

# Install the Python packages inside the image
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API and RAG Python files
COPY src ./src

# Copy the populated vector database
COPY chroma_db ./chroma_db

# Start the FastAPI web server when the container runs
CMD ["sh", "-c", "uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
