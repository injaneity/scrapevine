import requests
import os
from dotenv import load_dotenv
load_dotenv()

def product_search(tags, link):
    
    search_url = "https://www.googleapis.com/customsearch/v1"
    webpage_urls = []
    num_results_per_page = 5
    for page_num in range(0, 2):
        start_index = (page_num * num_results_per_page) + 1
        params = {
            'q': f"{tags} site:{link}",
            'cx': os.getenv("PSE_ID"),
            'searchType': 'image',
            'key': os.getenv("PSE_API"),
            'start': start_index,
            'num': num_results_per_page
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
        #webpage_urls = list(dict.fromkeys(webpage_urls)) # Remove duplicate links

        # Check if there are no more results
        if 'nextPage' not in result.get('queries', {}):
            break
    print("Links found: ", str(webpage_urls))
    return webpage_urls



