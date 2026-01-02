FROM python:3.11-slim

# Set working directory
WORKDIR /app

# install netcat for waiting on postgres
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*


# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Create SSH host key directory and generate key if missing
RUN mkdir -p /app/host_key_dir && \
    ssh-keygen -t rsa -b 2048 -f /app/host_key_dir/host_key -N "" || true

# Expose FastAPI port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
