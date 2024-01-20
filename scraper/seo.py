import requests

import os
from dotenv import load_dotenv
load_dotenv()

import time
start = time.time()

def google_image_search(query, site, api_key, cse_id, total_results=80):
    
    search_url = "https://www.googleapis.com/customsearch/v1"
    webpage_urls = []
    for start_index in range(1, total_results, 10):
        params = {
            'q': f"{query} site:{site}",
            'cx': cse_id,
            'searchType': 'image',
            'key': api_key,
            'start': start_index,
            'num': 10
        }
        response = requests.get(search_url, params=params)
        result = ""
        if response.status_code == 403:
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

# Example usage
api_key = os.getenv('PSE_API')
cse_id = os.getenv('PSE_ID')
tags = ['blue', 'shoes', 'leather']
site = 'charleskeith.com/sg'  # Specify the site for the search
webpage_results = google_image_search(tags, site, api_key, cse_id)

for url in webpage_results:
    print(url)
    
print(len(webpage_results))
    
print("--- %s seconds ---\n" % (time.time() - start))


