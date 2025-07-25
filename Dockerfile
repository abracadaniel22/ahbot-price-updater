# Official Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    lua5.3 \
    lua-dkjson \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory and copy files
WORKDIR /usr/src/app
COPY app.py .
COPY modules/*.py ./modules/
#COPY etc/ ./etc/
COPY requirements.txt .
COPY VERSION .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint
CMD ["python", "app.py"]