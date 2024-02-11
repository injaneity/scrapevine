from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setting up Chrome WebDriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless') # Uncomment if you don't need a browser UI
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Adjust these waits as necessary
driver.implicitly_wait(10) # Implicit wait for 10 seconds for elements to appear

try:
    # Open the webpage
    driver.get('https://www.pazzion.com/collections/shoes-flats/products/a1618-32-floret-ballerinas?variant=43368602796275')
    # Wait for the page to load dynamically. Adjust the condition as necessary.
    # Example: Wait for a specific element that indicates the page has loaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Now that the page is loaded, extract the HTML
    html_content = driver.page_source
    with open('./data.txt', 'w', encoding='utf-8') as file:
        file.write(html_content)

finally:
    driver.quit()
    
print("hello??")


# The `html_content` variable now contains the HTML of the page
