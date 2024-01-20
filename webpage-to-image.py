from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Initialize a Chrome session
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode, no UI is displayed
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage
url = 'https://www.lovebonito.com/sg/mira-knit-midi-dress.html'
driver.get(url)

# Set the window size to capture the entire page
driver.set_window_size(1920, driver.execute_script('return document.body.parentNode.scrollWidth'))
driver.set_window_size(1920, driver.execute_script('return document.body.parentNode.scrollHeight'))

# Define the path to the Downloads folder (this is for Windows, adjust for other OS)
downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'webpage_screenshot.png')

# Save the screenshot as a PNG file to the Downloads folder
driver.save_screenshot(downloads_path)

# Close the browser
driver.quit()
