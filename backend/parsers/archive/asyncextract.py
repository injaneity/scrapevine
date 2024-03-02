import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def html_extract(url):
    print(f"Extracting from {url}")
    options = webdriver.ChromeOptions()
    #options.add_argument('--incognito')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(5)
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        html_content = driver.page_source
    finally:
        driver.quit()
    return html_content

async def run_html_extract(executor, url):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, html_extract, url)

async def main(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = await asyncio.gather(*(run_html_extract(executor, url) for url in urls))
        return results