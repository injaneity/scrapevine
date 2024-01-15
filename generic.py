import requests
from bs4 import BeautifulSoup
import pandas as pd
import re  # Import the regular expressions module

def scrape_shoes(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve the website"

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Use regular expression to find all divs containing 'product' in their class
    product_regex = re.compile('.*product-.*')
    products = soup.find_all('div', class_=product_regex)
    
    name_regex = re.compile('.*(title|name|product-name).*')
    price_regex = re.compile('.*price.*')


    data = []
    for product in products:
        # Extracting product name and price
        name_tag = product.find('a', class_=name_regex)
        price_tag = product.find('div', class_=price_regex)

        if name_tag and price_tag:
            name = name_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            data.append({'Product Name': name, 'Price': price})

    df = pd.DataFrame(data)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)


    return df

# Usage example
url = 'https://www.pazzion.com/collections/shoes-flats'
df = scrape_shoes(url)

# Output the data
print(df)

# Optionally, save to an Excel file
df.to_excel('pazzion_shoes.xlsx', index=False)
