# 1) base Python 3.12
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# 2) install system tools including jq
RUN apt-get update && apt-get install -y \
      wget \
      curl \
      jq \
      gnupg \
      unzip \
      fonts-liberation \
      libasound2 \
      libatk-bridge2.0-0 \
      libatk1.0-0 \
      libcups2 \
      libdbus-1-3 \
      libgdk-pixbuf2.0-0 \
      libnspr4 \
      libnss3 \
      libx11-xcb1 \
      libxcomposite1 \
      libxdamage1 \
      libxrandr2 \
      xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# 3) install Google Chrome
RUN wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt-get update \
  && apt-get install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

# 4) install matching ChromeDriver via Chrome for Testing manifest
RUN CHROME_VER=$(google-chrome --version | sed -E 's/Google Chrome //') \
  && JSON=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json) \
  && DRIVER_URL=$(echo "$JSON" \
        | jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64").url') \
  && wget -q -O /tmp/chromedriver.zip "$DRIVER_URL" \
  && unzip /tmp/chromedriver.zip -d /tmp/ \
  && mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver \
  && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# 5) set workdir and install Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6) copy code and default command
COPY . .
CMD ["python", "browser-test.py"]
