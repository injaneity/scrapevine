from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_image(url):
    # Initialize a Chrome session
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode, no UI is displayed
    options.add_argument("--disable-gpu")  # Necessary for some versions of Chrome
    options.add_argument("--no-sandbox")  # Bypass OS security model, required on Heroku
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--window-size=1152,1152")  # Set appropriate window size
    options.add_argument("--force-device-scale-factor=1.1")  # Zoom in by 110%
    options.add_argument("--hide-scrollbars")  # Hide scrollbars to avoid them appearing in screenshots
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36")
    # options.add_extension("1.1.4_0.crx")
    # options.add_extension("1.55.0_0.crx")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)

    # Open the webpage
    driver.get(url)
    time.sleep(3)

    # Save the screenshot as a PNG file to the Downloads folder
    driver.save_screenshot('webpage_screenshot.png')

    # Close the browser
    driver.quit()
