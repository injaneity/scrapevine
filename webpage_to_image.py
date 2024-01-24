from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_image(url):
    # Initialize a Chrome session
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode, no UI is displayed
    options.add_argument("--disable-gpu")  # Necessary for some versions of Chrome
    options.add_argument("--no-sandbox")  # Bypass OS security model, required on Heroku
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--window-size=1536,1536")  # Set appropriate window size
    options.add_argument("--force-device-scale-factor=1.1")  # Zoom in by 110%
    options.add_argument("--hide-scrollbars")  # Hide scrollbars to avoid them appearing in screenshots
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open the webpage
    driver.get(url)

    # Save the screenshot as a PNG file to the Downloads folder
    driver.save_screenshot('webpage_screenshot.png')

    # Close the browser
    driver.quit()
