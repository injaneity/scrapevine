import requests

import os


import time
start = time.time()

def product_search(query, site, api_key, cse_id):
    
    search_url = "https://www.googleapis.com/customsearch/v1"
    webpage_urls = []
    for start_index in range(1, 2):
        params = {
            'q': f"{query} site:{site}",
            'cx': cse_id,
            'searchType': 'image',
            'key': api_key,
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

        # Check if there are no more results
        if 'nextPage' not in result.get('queries', {}):
            break

    return webpage_urls

'''
# Example usage
api_key = 'AIzaSyC8JhE_upi0lFOpDmN5xTdna5Dzh_RBH5I'
cse_id = 'b4d45415c77044fae'
tags = ['blue', 'shoes', 'leather']
site = 'charleskeith.com/sg'  # Specify the site for the search
webpage_results = product_search(tags, site, api_key, cse_id)

for url in webpage_results:
    print(url)
    
print(len(webpage_results))
    
print("--- %s seconds ---\n" % (time.time() - start))
'''
