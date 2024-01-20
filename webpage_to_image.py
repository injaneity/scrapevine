from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def get_image(url):
    # Initialize a Chrome session
    options = webdriver.ChromeOptions()
    options.headless = True  # Run in headless mode, no UI is displayed
    options.add_argument("--window-size=1350,1080")  # Set appropriate window size
    options.add_argument("--hide-scrollbars")  # Hide scrollbars to avoid them appearing in screenshots
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open the webpage
    driver.get(url)

    # Save the screenshot as a PNG file to the Downloads folder
    driver.save_screenshot('webpage_screenshot.png')

    # Close the browser
    driver.quit()
