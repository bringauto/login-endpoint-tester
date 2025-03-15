FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxrandr2 libgbm1 \
    libpango-1.0-0 libasound2 \
    libpangocairo-1.0-0 libxdamage1 libxshmfence1

# Install Playwright
RUN pip install playwright
RUN playwright install
RUN playwright install-deps

# Copy the Python script into the container
COPY test_login.py /app/test_login.py

# Set the working directory
WORKDIR /app
