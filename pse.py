import requests
import os


import time
start = time.time()

def product_search(query, site):
    
    search_url = "https://www.googleapis.com/customsearch/v1"
    webpage_urls = []
    for start_index in range(1, 4):
        params = {
            'q': f"{query} site:{site}",
            'cx': "b4d45415c77044fae",
            'searchType': 'image',
            'key': "AIzaSyC8JhE_upi0lFOpDmN5xTdna5Dzh_RBH5I",
            'start': start_index,
            'num': 1
        }
        response = requests.get(search_url, params=params)
        result = ""
        if response.status_code == 200:
            result = response.json()
        else:
            if response.status_code == 429:
                print("Error " + str(response.status_code) + ": Rate Limited Reached")
            else:
                print("Error " + str(response.status_code) + ": Unknown Issue")    
            return ""

        # Extracting webpage URLs where images are found
        webpage_urls.extend([item['image']['contextLink'] for item in result.get('items', [])])
        webpage_urls = list(dict.fromkeys(webpage_urls)) # Remove duplicate links

        # Check if there are no more results
        if 'nextPage' not in result.get('queries', {}):
            break
    print("Links found: ", str(webpage_urls))
    return webpage_urls