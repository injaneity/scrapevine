from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extract_html(url):
    #print(f"EXTRACTING FROM {url}")

    try:
        # Setting up Chrome WebDriver with options
        options = Options()
        options.add_argument('--headless') # Added for optimization
        options.add_argument('--disable-gpu') # Added for optimization
        options.add_argument('--incognito')
        options.add_argument('--no-sandbox')  # Added for optimization
        options.add_argument('--disable-dev-shm-usage')  # Added for optimization
        driver = webdriver.Chrome(options=options)

        driver.implicitly_wait(5)  # Implicit wait

        driver.get(url)
        
        # Explicit wait: Wait for the body element to be loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        # Extract the HTML content
        html_content = driver.page_source

        driver.quit()
    
    except:
        print("COULD NOT EXTRACT HTML, WEBDRIVER")
        return None
    
    return html_content
