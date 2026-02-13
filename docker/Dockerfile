# Use official Python 3.12.0 slim image
FROM python:3.12.0-slim

# Prevents Python from buffering stdout/stderr (useful for container logs)
ENV PYTHONUNBUFFERED=1 

# System dependencies needed to build some Python packages (psycopg2, numpy, scikit-learn)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user and app directory
ENV APP_HOME=/app
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR ${APP_HOME}

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ${APP_HOME}
RUN chown -R appuser:appuser ${APP_HOME}

# Create data directory for SQLite
RUN mkdir -p ${APP_HOME}/data && chown -R appuser:appuser ${APP_HOME}/data

USER appuser

# Expose port used by Uvicorn
EXPOSE 8000

# Default command to run the FastAPI app
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
