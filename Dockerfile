# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment variables for non-interactive Python & Streamlit execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# Install system dependencies required for compilation and openpyxl/numpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy enterprise platform codebase
COPY . .

# Ensure data and models persistence folders exist
RUN mkdir -p data models

# Expose standard Streamlit port
EXPOSE 8501

# Healthcheck to verify Tornado server liveliness
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch persistent Streamlit server process
CMD ["streamlit", "run", "app.py"]
