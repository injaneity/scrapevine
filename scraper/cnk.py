import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_shoes(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve the website"

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Assuming product details are contained in 'product-tile' class
    products = soup.find_all('div', class_='product-tile')

    data = []
    for product in products:
        # Extracting product name and price
        name_tag = product.find('a', class_='js-product_tile-name')
        price_tag = product.find('div', class_='price')

        if name_tag and price_tag:
            name = name_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            data.append({'Product Name': name, 'Price': price})

    return pd.DataFrame(data)

# Usage
url = 'https://www.charleskeith.com/sg/shoes'
df = scrape_shoes(url)

# Output the data
print(df)

# Optionally, save to an Excel file
df.to_excel('charleskeith_shoes.xlsx', index=False)
