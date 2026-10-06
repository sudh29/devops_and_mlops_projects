# Start from selenium/standalone-chrome
FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /app

# Install pip and dependencies safely, clean cache
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copy test files and set permissions for seluser
COPY . .
RUN chown -R seluser:seluser /app

# Switch back to non-root seluser
USER seluser

# Set the default command
CMD ["python3", "browser-test.py"]
