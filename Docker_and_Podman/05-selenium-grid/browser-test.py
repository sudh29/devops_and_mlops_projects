"""
Remote Selenium Grid integration test.
Supports multi-browser testing (Chrome, Firefox, Edge) with explicit waits and assertions.
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

GRID_URL = os.getenv("GRID_URL", "http://localhost:4444/wd/hub")
BROWSER = os.getenv("BROWSER", "chrome").lower()

def get_remote_driver(browser_name: str) -> webdriver.Remote:
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    return webdriver.Remote(command_executor=GRID_URL, options=options)

def run_test():
    driver = get_remote_driver(BROWSER)
    try:
        print(f"Connecting to Grid at {GRID_URL} with browser {BROWSER}...")
        driver.get("https://www.google.com")
        assert "Google" in driver.title, f"Unexpected title: {driver.title}"
        print(f"[PASS] Page title loaded: {driver.title}")

        wait = WebDriverWait(driver, 15)
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
        search_box.send_keys(f"Selenium Grid {BROWSER.capitalize()} Test")
        search_box.submit()

        wait.until(EC.title_contains("Selenium Grid"))
        assert "Selenium Grid" in driver.title, f"Search title mismatch: {driver.title}"
        print(f"[PASS] Search results loaded for {BROWSER} successfully.")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
