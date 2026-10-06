"""
Headless browser automation test using Selenium.
Includes explicit waits and assertions.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
CHROME_BINARY_PATH = os.environ.get("CHROME_BINARY_PATH", "/usr/bin/google-chrome")

def test_google_search():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")

    if os.path.exists(CHROME_BINARY_PATH):
        options.binary_location = CHROME_BINARY_PATH

    service = Service(CHROMEDRIVER_PATH) if os.path.exists(CHROMEDRIVER_PATH) else None
    driver = webdriver.Chrome(service=service, options=options) if service else webdriver.Chrome(options=options)

    try:
        driver.get("https://www.google.com")
        assert "Google" in driver.title, f"Unexpected title: {driver.title}"
        print(f"[PASS] Initial page title verified: {driver.title}")

        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
        search_box.send_keys("Selenium Docker Testing")
        search_box.submit()

        wait.until(EC.title_contains("Selenium"))
        assert "Selenium" in driver.title, f"Search title mismatch: {driver.title}"
        print(f"[PASS] Search results loaded with title: {driver.title}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_google_search()
