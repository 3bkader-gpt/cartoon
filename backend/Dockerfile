FROM python:3.12-slim

# System deps for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt \
    && python -m playwright install --with-deps chromium

# Copy backend code
COPY backend/ /app/backend/

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["python", "backend/main.py"]
