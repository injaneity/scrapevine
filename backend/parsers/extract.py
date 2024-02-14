from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# Include the accept_cookies call in your html_extract function after loading the page
def html_extract(url):
    
    print(f"Extracting from {url}")

    # Setting up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')  # Enable incognito mode
    #options.add_argument('--headless') # Uncomment if you don't need a browser UI
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(5)  # Implicit wait

    try:
        driver.get(url)
        # Wait for the page to load dynamically, then accept cookies
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        # Extract the HTML content
        html_content = driver.page_source
    finally:
        driver.quit()
        
    return html_content
