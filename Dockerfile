FROM python:3.10-slim

WORKDIR /app

# Install system dependencies: OpenMP for fastembed + build tools for C++ extension
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    build-essential \
    cmake \
    pybind11-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the embedding model into the image
RUN python -c "from fastembed import TextEmbedding; TextEmbedding(model_name='BAAI/bge-small-en-v1.5')"

# Copy the application source
COPY . .

# Build the C++ extension (pybind11 must be installed as a pip package for setup.py)
RUN pip install pybind11 && pip install -e src/

# Render sets $PORT automatically; fall back to 7860 for Hugging Face Spaces
EXPOSE 7860
CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-7860}