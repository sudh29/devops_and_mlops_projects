from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Tell Selenium explicitly where chromedriver is
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"  # default path in selenium/standalone-chrome
CHROME_BINARY_PATH = "/usr/bin/google-chrome"  # optional, if needed

# Set Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')  # comment this if you want to see GUI

# Point to correct Chrome binary (optional, usually not needed)
options.binary_location = CHROME_BINARY_PATH

# Create WebDriver manually using Service object
from selenium.webdriver.chrome.service import Service

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open Google
    driver.get("https://www.google.com")
    print("Page title is:", driver.title)

    time.sleep(2)

    # Perform a search
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Podman Selenium Test")
    search_box.submit()

    time.sleep(2)
    print("New page title is:", driver.title)

finally:
    # Quit the driver
    driver.quit()
